"""
AGENT--SITE--DNA: Unified CLI
Runs the full pipeline: Extract → Analyze → Recommend.

Usage:
    python run.py <url>                         # Extract + Motion strategy
    python run.py <url> --output ./my_brands    # Custom output dir
    python run.py <url> --pages 6               # Scan up to 6 pages
    python run.py --motion <path/to/dna.json>   # Motion strategy only
"""

__version__ = "1.0.0"

import sys
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        prog="AGENT--SITE--DNA",
        description="Autonomous Brand DNA Extraction & Motion Architecture",
    )
    parser.add_argument("url", nargs="?", help="Target website URL")
    parser.add_argument("--output", "-o", type=str, default=None,
                        help="Output base directory")
    parser.add_argument("--pages", "-p", type=int, default=4,
                        help="Max pages to scan (default: 4)")
    parser.add_argument("--motion", "-m", type=str, default=None,
                        help="Run Motion Architect on existing dna.json (skip extraction)")
    args = parser.parse_args()

    # Mode 1: Motion-only
    if args.motion:
        from DNA_MOTION_ARCHITECT import analyze_motion
        analyze_motion(args.motion)
        return

    # Mode 2: Full pipeline
    if not args.url:
        parser.print_help()
        sys.exit(1)

    import nexus_visual_analyzer as extractor

    if args.output:
        extractor.BASE_DIR = Path(args.output)

    target = args.url
    if not target.startswith("http"):
        target = "https://" + target

    # Step 1: Extract DNA
    dna, out_dir = extractor.run(target, max_pages=args.pages)
    dna_path = out_dir / "dna.json"

    # Step 2: Generate Motion Strategy
    from DNA_MOTION_ARCHITECT import analyze_motion
    analyze_motion(str(dna_path))

    print(f"\n[OK] Full pipeline complete → {out_dir}")
    print(f"     ├── dna.json")
    print(f"     ├── brandbook.html")
    print(f"     ├── copy_dna.md")
    print(f"     └── motion_strategy.md")


if __name__ == "__main__":
    main()
