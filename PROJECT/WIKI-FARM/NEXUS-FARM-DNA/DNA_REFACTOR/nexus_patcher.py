#!/usr/bin/env python3
"""
NEXUS Post-Synthesis Patcher
"Прививка от родовых травм"

Находит и исправляет системные баги синтезированных агентов NEXUS:
  1. Потеря данных между стейджами (_result= вместо extend)
  2. Контракт render()/run() возвращает dict вместо str
  3. Артефакт text_similarity на нестроковых данных
  4. Дублирующиеся импорты
  5. Конфликт типов target между блоками

Использование:
  python nexus_patcher.py --dir ./agents            # отчёт по всей папке
  python nexus_patcher.py --dir ./agents --patch     # исправить все файлы
  python nexus_patcher.py --file agent.py --patch    # исправить один файл
"""

import re
import ast
import sys
import shutil
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Tuple, Optional


# ─────────────────────────────────────────────
#  Структуры данных
# ─────────────────────────────────────────────

@dataclass
class Issue:
    code: str          # ID бага
    severity: str      # CRITICAL / WARNING / INFO
    line: int          # номер строки
    description: str   # что не так
    fix: str           # что будет сделано


@dataclass
class FileReport:
    path: Path
    issues: List[Issue] = field(default_factory=list)
    patched: bool = False
    patch_error: Optional[str] = None

    @property
    def has_issues(self) -> bool:
        return len(self.issues) > 0

    def summary(self) -> str:
        crits = sum(1 for i in self.issues if i.severity == "CRITICAL")
        warns = sum(1 for i in self.issues if i.severity == "WARNING")
        return f"{crits} CRITICAL, {warns} WARNING, {len(self.issues) - crits - warns} INFO"


# ─────────────────────────────────────────────
#  Детекторы багов
# ─────────────────────────────────────────────

def detect_lost_data(lines: List[str]) -> List[Issue]:
    """
    БАГ-1: Результат функции кладётся в _result но не добавляется в self.findings/all_findings.
    Паттерн: строка вида `_result = some_func(...)` без последующего extend/append.
    """
    issues = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Находим присвоение _result
        m = re.match(r'\s*_result\s*=\s*(\w+)\s*\(', line)
        if m:
            func_name = m.group(1)
            # Смотрим следующие 3 строки — есть ли extend/append?
            window = lines[i+1:i+4]
            has_extend = any(
                re.search(r'(self\.\w+findings\b|self\.findings)\s*\.\s*(extend|append)\s*\(_result\)', l)
                for l in window
            )
            # Также проверяем паттерн сохранения в stats
            has_stats = any(
                re.search(r'self\.\w+stats\b.*=.*_result', l)
                for l in window
            )
            if not has_extend and not has_stats:
                issues.append(Issue(
                    code="LOST_DATA",
                    severity="CRITICAL",
                    line=i + 1,
                    description=f"Результат {func_name}() присвоен _result, но не добавлен в findings/stats",
                    fix="Добавить self.all_findings.extend(_result) или self.findings.extend(_result)"
                ))
        i += 1
    return issues


def detect_contract_mismatch(lines: List[str]) -> List[Issue]:
    """
    БАГ-2: Метод render()/run() объявлен как -> str но возвращает dict.
    """
    issues = []
    for i, line in enumerate(lines):
        # Ищем объявление метода с аннотацией -> str
        if re.search(r'def\s+(render|run)\s*\(.*\)\s*->\s*str\s*:', line):
            # Ищем return { в следующих 200 строках
            for j in range(i+1, min(i+200, len(lines))):
                if re.match(r'\s*return\s*\{', lines[j]):
                    issues.append(Issue(
                        code="CONTRACT_MISMATCH",
                        severity="WARNING",
                        line=i + 1,
                        description=f"Метод объявлен как -> str, но возвращает dict (строка {j+1})",
                        fix="Исправить аннотацию на -> Dict[str, Any]"
                    ))
                    break
                # Выходим из scope метода если встретили другой def
                if re.match(r'\s*def\s+', lines[j]) and j > i + 1:
                    break
    return issues


def detect_text_similarity_artifact(lines: List[str]) -> List[Issue]:
    """
    БАГ-3: text_similarity вызывается на нестроковых данных (str(target) где target — URL или список).
    """
    issues = []
    for i, line in enumerate(lines):
        if re.search(r'text_similarity\s*\(\s*str\s*\(\s*target\s*\)\s*\)', line):
            issues.append(Issue(
                code="TEXT_SIM_ARTIFACT",
                severity="WARNING",
                line=i + 1,
                description="text_similarity(str(target)) — вызов на строке target не имеет смысла для URL/hostname",
                fix="Удалить вызов или заменить на осмысленный текстовый ввод"
            ))
    return issues


def detect_duplicate_imports(lines: List[str]) -> List[Issue]:
    """
    БАГ-4: Один и тот же модуль импортируется дважды.
    """
    issues = []
    seen = {}
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("import ") or stripped.startswith("from "):
            # Нормализуем строку импорта
            key = re.sub(r'\s+', ' ', stripped)
            if key in seen:
                issues.append(Issue(
                    code="DUPLICATE_IMPORT",
                    severity="INFO",
                    line=i + 1,
                    description=f"Дублирующийся импорт: '{stripped}' (первый раз на строке {seen[key]+1})",
                    fix="Удалить дублирующую строку импорта"
                ))
            else:
                seen[key] = i
    return issues


def detect_type_conflict(lines: List[str]) -> List[Issue]:
    """
    БАГ-5: Конфликт типов target — функция с Path-сигнатурой получает str.
    Упрощённая эвристика: ищем analyze_csv(str(target)) или Path(target) смешанные с URL-функциями.
    """
    issues = []
    has_url_func = any(
        re.search(r'def\s+(extract_links|http_fingerprint|probe_endpoints|dns_recon)\s*\(', l)
        for l in lines
    )
    has_path_func = any(
        re.search(r'def\s+(analyze_csv|store_findings_db)\s*\(', l)
        for l in lines
    )

    if has_url_func and has_path_func:
        # Ищем где analyze_csv вызывается со str(target)
        for i, line in enumerate(lines):
            if re.search(r'analyze_csv\s*\(\s*str\s*\(\s*target\s*\)\s*\)', line):
                issues.append(Issue(
                    code="TYPE_CONFLICT",
                    severity="CRITICAL",
                    line=i + 1,
                    description="analyze_csv ожидает Path, но получает str(target). "
                                "Агент смешивает URL-домен и файловый домен",
                    fix="Обернуть в Path(): analyze_csv(Path(str(target)))"
                ))

    return issues


# ─────────────────────────────────────────────
#  Патчеры
# ─────────────────────────────────────────────

def patch_lost_data(source: str) -> str:
    """
    Исправляет БАГ-1: добавляет extend после _result = func() если его нет.
    Определяет имя поля findings из класса (self.findings или self.all_findings).
    """
    lines = source.splitlines()
    result_lines = []
    i = 0

    # Определяем имя поля findings в классе
    findings_field = "all_findings"
    for line in lines:
        if re.search(r'self\.findings\s*=\s*\[\]', line):
            findings_field = "findings"
            break
        if re.search(r'self\.all_findings\s*=\s*\[\]', line):
            findings_field = "all_findings"
            break

    while i < len(lines):
        line = lines[i]
        result_lines.append(line)

        m = re.match(r'(\s*)_result\s*=\s*(\w+)\s*\(', line)
        if m:
            indent = m.group(1)
            func_name = m.group(2)

            # Проверяем следующие 3 строки
            window = lines[i+1:i+4]
            has_extend = any(
                re.search(r'(self\.\w*findings)\s*\.\s*(extend|append)\s*\(_result\)', l)
                for l in window
            )
            has_stats = any(
                re.search(r'self\.\w*stats.*=.*_result', l)
                for l in window
            )

            if not has_extend and not has_stats:
                # Определяем что вставить — list или dict возвращает функция
                # Эвристика: если функция заканчивается на _stats, _info — это dict
                # Или если есть process_list, analyze, scan - list
                if re.search(r'(stats|info|summary)$', func_name, re.IGNORECASE):
                    result_lines.append(
                        f"{indent}# [PATCHER] Сохранено из {func_name}"
                    )
                    result_lines.append(
                        f"{indent}if isinstance(_result, dict): self.all_stats.update(_result)"
                    )
                else:
                    result_lines.append(
                        f"{indent}# [PATCHER] Восстановлена передача данных из {func_name}"
                    )
                    result_lines.append(
                        f"{indent}if isinstance(_result, list): self.{findings_field}.extend(_result)"
                    )
        i += 1

    return "\n".join(result_lines)


def patch_contract_mismatch(source: str) -> str:
    """Исправляет БАГ-2: -> str меняет на -> Dict[str, Any]"""
    return re.sub(
        r'(def\s+(?:render|run)\s*\(.*?\))\s*->\s*str\s*:',
        r'\1 -> Dict[str, Any]:',
        source
    )


def patch_text_similarity_artifact(source: str) -> str:
    """Исправляет БАГ-3: комментирует бессмысленный вызов text_similarity"""
    lines = source.splitlines()
    result = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if re.search(r'text_similarity\s*\(\s*str\s*\(\s*target\s*\)\s*\)', line):
            indent = re.match(r'(\s*)', line).group(1)
            result.append(f"{indent}# [PATCHER] Удалён артефакт text_similarity(str(target))")
            result.append(f"{indent}# {line.strip()}")
        else:
            result.append(line)
        i += 1
    return "\n".join(result)


def patch_duplicate_imports(source: str) -> str:
    """Исправляет БАГ-4: удаляет дублирующиеся строки импортов"""
    lines = source.splitlines()
    seen = set()
    result = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("import ") or stripped.startswith("from "):
            key = re.sub(r'\s+', ' ', stripped)
            if key in seen:
                result.append(f"# [PATCHER] Удалён дублирующийся импорт: {stripped}")
                continue
            seen.add(key)
        result.append(line)
    return "\n".join(result)


def patch_type_conflict(source: str) -> str:
    """Исправляет БАГ-5: оборачивает analyze_csv(str(target)) в Path()"""
    return re.sub(
        r'analyze_csv\s*\(\s*str\s*\(\s*target\s*\)\s*\)',
        'analyze_csv(Path(str(target)))',
        source
    )


# ─────────────────────────────────────────────
#  Основная логика
# ─────────────────────────────────────────────

ALL_DETECTORS = [
    detect_lost_data,
    detect_contract_mismatch,
    detect_text_similarity_artifact,
    detect_duplicate_imports,
    detect_type_conflict,
]

ALL_PATCHERS = [
    patch_duplicate_imports,       # сначала — не меняет структуру
    patch_contract_mismatch,
    patch_text_similarity_artifact,
    patch_type_conflict,
    patch_lost_data,               # последним — зависит от структуры
]


def analyze_file(path: Path) -> FileReport:
    report = FileReport(path=path)
    try:
        source = path.read_text(encoding="utf-8")
        lines = source.splitlines()
        for detector in ALL_DETECTORS:
            report.issues.extend(detector(lines))
    except Exception as e:
        report.patch_error = f"Ошибка чтения: {e}"
    return report


def patch_file(path: Path, dry_run: bool = False) -> FileReport:
    report = analyze_file(path)

    if not report.has_issues:
        return report

    try:
        source = path.read_text(encoding="utf-8")
        patched = source

        for patcher in ALL_PATCHERS:
            patched = patcher(patched)

        if not dry_run:
            # Бэкап оригинала
            backup = path.with_suffix(".py.bak")
            shutil.copy2(path, backup)
            path.write_text(patched, encoding="utf-8")

        report.patched = True

    except Exception as e:
        report.patch_error = str(e)

    return report


def process_directory(dir_path: Path, do_patch: bool = False) -> List[FileReport]:
    reports = []
    agents = sorted(dir_path.rglob("*.py"))

    if not agents:
        print(f"  Нет .py файлов в {dir_path}")
        return reports

    for agent_path in agents:
        if agent_path.name.endswith(".bak.py"):
            continue
        if do_patch:
            report = patch_file(agent_path)
        else:
            report = analyze_file(agent_path)
        reports.append(report)

    return reports


def print_report(reports: List[FileReport], verbose: bool = False):
    total_issues = sum(len(r.issues) for r in reports)
    total_files = len(reports)
    files_with_issues = sum(1 for r in reports if r.has_issues)

    print(f"\n{'='*60}")
    print(f"NEXUS PATCHER — Отчёт")
    print(f"{'='*60}")
    print(f"Файлов проверено : {total_files}")
    print(f"Файлов с багами  : {files_with_issues}")
    print(f"Всего проблем    : {total_issues}")
    print(f"{'='*60}\n")

    for report in reports:
        if not report.has_issues and not verbose:
            continue

        status = "[OK]" if not report.has_issues else "[X]"
        patched_mark = " [PATCHED]" if report.patched else ""
        print(f"  {status} {report.path.name}{patched_mark}")

        if report.patch_error:
            print(f"    ! Error: {report.patch_error}")

        for issue in report.issues:
            icon = "[!]" if issue.severity == "CRITICAL" else "[W]" if issue.severity == "WARNING" else "[I]"
            print(f"    {icon} [{issue.code}] line {issue.line}: {issue.description}")
            if verbose:
                print(f"       -> Fix: {issue.fix}")

        if report.issues:
            print()

    # Статистика по типам багов
    from collections import Counter
    all_issues = [i for r in reports for i in r.issues]
    if all_issues:
        print(f"{'-'*40}")
        print("Распределение по типам:")
        for code, count in Counter(i.code for i in all_issues).most_common():
            print(f"  {code:30s} {count}")
        print()


# ─────────────────────────────────────────────
#  CLI
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="NEXUS Post-Synthesis Patcher — прививка от родовых травм",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
  python nexus_patcher.py --dir ./agents
  python nexus_patcher.py --dir ./agents --patch
  python nexus_patcher.py --file agent.py --patch --verbose
        """
    )
    parser.add_argument("--dir",  type=Path, help="Папка с агентами")
    parser.add_argument("--file", type=Path, help="Один файл агента")
    parser.add_argument("--patch", action="store_true", help="Применить патчи (иначе только отчёт)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Показать описание фиксов")
    args = parser.parse_args()

    if not args.dir and not args.file:
        parser.error("Укажите --dir или --file")

    reports = []

    if args.dir:
        if not args.dir.exists():
            print(f"Папка не найдена: {args.dir}")
            sys.exit(1)
        reports = process_directory(args.dir, do_patch=args.patch)

    elif args.file:
        if not args.file.exists():
            print(f"Файл не найден: {args.file}")
            sys.exit(1)
        if args.patch:
            reports = [patch_file(args.file)]
        else:
            reports = [analyze_file(args.file)]

    print_report(reports, verbose=args.verbose)

    if args.patch:
        patched = sum(1 for r in reports if r.patched)
        print(f"Пропатчено файлов: {patched}")
        print("Оригиналы сохранены с расширением .py.bak")


if __name__ == "__main__":
    main()
