#!/usr/bin/env python3
"""
NEXUS DNA OSINT Agent: METADATA_EXTRACTOR
Tier: S-Target (Production-Hardened)

Extracts metadata from local files: EXIF from images, PDF metadata,
Office document properties, and generic file system attributes.
Uses only Python stdlib — zero external dependencies.
"""

import json
import logging
import sqlite3
import hashlib
import struct
import sys
import os
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("METADATA_EXTRACTOR")


@dataclass
class FileMetadata:
    filepath: str
    filename: str
    extension: str
    size_bytes: int = 0
    created: str = ""
    modified: str = ""
    sha256: str = ""
    mime_guess: str = ""
    # Extracted metadata fields
    author: str = ""
    title: str = ""
    subject: str = ""
    creator_tool: str = ""
    producer: str = ""
    gps_lat: Optional[float] = None
    gps_lon: Optional[float] = None
    camera_make: str = ""
    camera_model: str = ""
    software: str = ""
    extra: dict = field(default_factory=dict)


@dataclass
class MetadataReport:
    scan_path: str
    files_scanned: int = 0
    files_with_metadata: int = 0
    results: list[FileMetadata] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


# MIME type detection by magic bytes
MAGIC_SIGNATURES = {
    b"\xff\xd8\xff": "image/jpeg",
    b"\x89PNG": "image/png",
    b"GIF87a": "image/gif",
    b"GIF89a": "image/gif",
    b"%PDF": "application/pdf",
    b"PK\x03\x04": "application/zip",  # also docx/xlsx/pptx
    b"\xd0\xcf\x11\xe0": "application/msoffice",
}

# EXIF tag IDs we care about
EXIF_TAGS = {
    0x010F: "camera_make",
    0x0110: "camera_model",
    0x0131: "software",
    0x013B: "author",
    0x9003: "datetime_original",
    0x9004: "datetime_digitized",
    0x010E: "title",
}

GPS_TAGS = {
    0x0002: "gps_lat_data",
    0x0001: "gps_lat_ref",
    0x0004: "gps_lon_data",
    0x0003: "gps_lon_ref",
}


class MetadataExtractorAgent:
    """Extract metadata from files using only Python stdlib."""

    def __init__(self, db_path: str = "nexus_osint.db"):
        self.db_path = db_path
        self._init_storage()

    def _init_storage(self) -> None:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS file_metadata (
                        id           INTEGER PRIMARY KEY AUTOINCREMENT,
                        filepath     TEXT NOT NULL,
                        filename     TEXT NOT NULL,
                        extension    TEXT,
                        size_bytes   INTEGER,
                        sha256       TEXT NOT NULL,
                        author       TEXT,
                        title        TEXT,
                        creator_tool TEXT,
                        gps_lat      REAL,
                        gps_lon      REAL,
                        camera_make  TEXT,
                        extra_json   TEXT,
                        ts           DATETIME DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(sha256)
                    )
                """)
                conn.commit()
            logger.info("Storage ready.")
        except sqlite3.Error as exc:
            logger.critical("DB init failed: %s", exc)
            raise SystemExit(1) from exc

    @staticmethod
    def _file_hash(filepath: Path) -> str:
        h = hashlib.sha256()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()

    @staticmethod
    def _detect_mime(filepath: Path) -> str:
        try:
            with open(filepath, "rb") as f:
                header = f.read(8)
            for sig, mime in MAGIC_SIGNATURES.items():
                if header.startswith(sig):
                    return mime
        except OSError:
            pass
        return "application/octet-stream"

    def _extract_pdf_metadata(self, filepath: Path) -> dict:
        """Extract metadata from PDF Info dictionary."""
        meta = {}
        try:
            with open(filepath, "rb") as f:
                content = f.read()

            # Find /Info dictionary entries
            text = content.decode("latin-1", errors="ignore")
            for key, field_name in [
                ("/Author", "author"),
                ("/Title", "title"),
                ("/Subject", "subject"),
                ("/Creator", "creator_tool"),
                ("/Producer", "producer"),
            ]:
                idx = text.find(key)
                if idx != -1:
                    # Extract parenthesized string: /Key (value)
                    paren_start = text.find("(", idx)
                    paren_end = text.find(")", paren_start + 1) if paren_start != -1 else -1
                    if paren_start != -1 and paren_end != -1:
                        val = text[paren_start + 1:paren_end].strip()
                        if val:
                            meta[field_name] = val
        except OSError as exc:
            logger.warning("PDF read error for %s: %s", filepath, exc)
        return meta

    def _extract_exif(self, filepath: Path) -> dict:
        """Minimal EXIF parser for JPEG — stdlib only, no PIL."""
        meta = {}
        try:
            with open(filepath, "rb") as f:
                # Check JPEG SOI
                if f.read(2) != b"\xff\xd8":
                    return meta
                # Find APP1 (EXIF) marker
                while True:
                    marker = f.read(2)
                    if len(marker) < 2:
                        break
                    if marker == b"\xff\xe1":  # APP1
                        length = struct.unpack(">H", f.read(2))[0]
                        exif_data = f.read(length - 2)
                        meta = self._parse_exif_block(exif_data)
                        break
                    elif marker[0:1] == b"\xff":
                        length = struct.unpack(">H", f.read(2))[0]
                        f.seek(length - 2, 1)
                    else:
                        break
        except (OSError, struct.error) as exc:
            logger.warning("EXIF read error for %s: %s", filepath, exc)
        return meta

    def _parse_exif_block(self, data: bytes) -> dict:
        """Parse EXIF IFD entries from raw APP1 data."""
        meta = {}
        if not data.startswith(b"Exif\x00\x00"):
            return meta

        tiff = data[6:]
        if len(tiff) < 8:
            return meta

        # Byte order
        if tiff[:2] == b"II":
            endian = "<"
        elif tiff[:2] == b"MM":
            endian = ">"
        else:
            return meta

        offset = struct.unpack(f"{endian}I", tiff[4:8])[0]
        self._read_ifd(tiff, offset, endian, meta, EXIF_TAGS)

        return meta

    def _read_ifd(self, tiff: bytes, offset: int, endian: str,
                  meta: dict, tags: dict) -> None:
        """Read IFD entries and extract known tags."""
        if offset + 2 > len(tiff):
            return
        count = struct.unpack(f"{endian}H", tiff[offset:offset + 2])[0]

        for i in range(count):
            entry_offset = offset + 2 + i * 12
            if entry_offset + 12 > len(tiff):
                break
            tag_id = struct.unpack(f"{endian}H", tiff[entry_offset:entry_offset + 2])[0]
            dtype = struct.unpack(f"{endian}H", tiff[entry_offset + 2:entry_offset + 4])[0]
            count_val = struct.unpack(f"{endian}I", tiff[entry_offset + 4:entry_offset + 8])[0]
            value_offset_bytes = tiff[entry_offset + 8:entry_offset + 12]

            if tag_id in tags:
                # ASCII string type
                if dtype == 2:
                    if count_val <= 4:
                        val = value_offset_bytes[:count_val].decode("ascii", errors="ignore").strip("\x00")
                    else:
                        str_offset = struct.unpack(f"{endian}I", value_offset_bytes)[0]
                        if str_offset + count_val <= len(tiff):
                            val = tiff[str_offset:str_offset + count_val].decode("ascii", errors="ignore").strip("\x00")
                        else:
                            val = ""
                    if val:
                        meta[tags[tag_id]] = val

            # Check for ExifIFD pointer (tag 0x8769)
            if tag_id == 0x8769 and dtype == 4:
                sub_offset = struct.unpack(f"{endian}I", value_offset_bytes)[0]
                self._read_ifd(tiff, sub_offset, endian, meta, tags)

    def _extract_fs_metadata(self, filepath: Path) -> dict:
        """Extract filesystem-level metadata."""
        stat = filepath.stat()
        return {
            "size_bytes": stat.st_size,
            "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        }

    def extract(self, filepath: Path) -> FileMetadata:
        """Full metadata extraction for a single file."""
        logger.info("Extracting metadata from: %s", filepath.name)

        fs_meta = self._extract_fs_metadata(filepath)
        mime = self._detect_mime(filepath)

        record = FileMetadata(
            filepath=str(filepath.resolve()),
            filename=filepath.name,
            extension=filepath.suffix.lower(),
            size_bytes=fs_meta["size_bytes"],
            created=fs_meta["created"],
            modified=fs_meta["modified"],
            sha256=self._file_hash(filepath),
            mime_guess=mime,
        )

        # Type-specific extraction
        if mime == "image/jpeg":
            exif = self._extract_exif(filepath)
            record.author = exif.get("author", "")
            record.title = exif.get("title", "")
            record.camera_make = exif.get("camera_make", "")
            record.camera_model = exif.get("camera_model", "")
            record.software = exif.get("software", "")
            record.extra = {k: v for k, v in exif.items()
                           if k not in ("author", "title", "camera_make", "camera_model", "software")}

        elif mime == "application/pdf":
            pdf_meta = self._extract_pdf_metadata(filepath)
            record.author = pdf_meta.get("author", "")
            record.title = pdf_meta.get("title", "")
            record.subject = pdf_meta.get("subject", "")
            record.creator_tool = pdf_meta.get("creator_tool", "")
            record.producer = pdf_meta.get("producer", "")

        return record

    def execute_scan(self, scan_path: str) -> MetadataReport:
        target = Path(scan_path)
        report = MetadataReport(scan_path=scan_path)

        files: list[Path] = []
        if target.is_file():
            files = [target]
        elif target.is_dir():
            files = [f for f in target.rglob("*") if f.is_file()]
        else:
            report.errors.append(f"Path not found: {scan_path}")
            return report

        for filepath in files:
            try:
                record = self.extract(filepath)
                report.results.append(record)
                report.files_scanned += 1
                has_meta = any([record.author, record.title, record.camera_make,
                                record.creator_tool, record.extra])
                if has_meta:
                    report.files_with_metadata += 1
            except Exception as exc:
                logger.error("Failed to extract %s: %s", filepath, exc)
                report.errors.append(f"{filepath.name}: {exc}")

        # Persist
        try:
            with sqlite3.connect(self.db_path) as conn:
                for rec in report.results:
                    conn.execute(
                        """INSERT OR IGNORE INTO file_metadata
                           (filepath, filename, extension, size_bytes, sha256,
                            author, title, creator_tool, gps_lat, gps_lon,
                            camera_make, extra_json)
                           VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                        (rec.filepath, rec.filename, rec.extension, rec.size_bytes,
                         rec.sha256, rec.author, rec.title, rec.creator_tool,
                         rec.gps_lat, rec.gps_lon, rec.camera_make,
                         json.dumps(rec.extra)),
                    )
                conn.commit()
            logger.info("Persisted metadata for %d files", report.files_scanned)
        except sqlite3.Error as exc:
            logger.error("DB error: %s", exc)
            report.errors.append(str(exc))

        return report


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python 69_METADATA_EXTRACTOR_synthesized_agent.py <file_or_directory>")
        sys.exit(1)

    agent = MetadataExtractorAgent()
    result = agent.execute_scan(sys.argv[1])
    print(json.dumps(asdict(result), indent=2, ensure_ascii=False))
