#!/usr/bin/env python3
"""Audit, repair and validate Jupyter notebooks for GitHub/Google Colab.

The main failure mode this script repairs is malformed JSON caused by literal
backslashes inside notebook JSON strings (very common when LaTeX such as \alpha,
\( ... \), etc. was written without JSON escaping). It also normalizes the
minimal nbformat structure required by Jupyter/Colab and validates every file
with nbformat.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import nbformat
from nbformat.validator import NotebookValidationError


VALID_SIMPLE_ESCAPES = {'"', '\\', '/', 'b', 'f', 'n', 'r', 't'}
HEX = set("0123456789abcdefABCDEF")


def repair_json_text(raw: str) -> tuple[str, int]:
    """Repair invalid JSON escapes/control chars only inside JSON strings.

    Unknown sequences such as ``\(``, ``\[``, ``\alpha`` or ``\mathbf`` are
    turned into literal backslashes by doubling the slash in the JSON text.
    Already-correct JSON escapes are preserved.
    """
    out: list[str] = []
    in_string = False
    fixes = 0
    i = 0

    while i < len(raw):
        ch = raw[i]

        if not in_string:
            out.append(ch)
            if ch == '"':
                in_string = True
            i += 1
            continue

        # Inside a JSON string.
        if ch == '"':
            out.append(ch)
            in_string = False
            i += 1
            continue

        if ch == '\\':
            if i + 1 >= len(raw):
                out.append('\\\\')
                fixes += 1
                i += 1
                continue

            nxt = raw[i + 1]
            if nxt in VALID_SIMPLE_ESCAPES:
                out.append(ch)
                out.append(nxt)
                i += 2
                continue

            if nxt == 'u':
                digits = raw[i + 2:i + 6]
                if len(digits) == 4 and all(c in HEX for c in digits):
                    out.append(raw[i:i + 6])
                    i += 6
                    continue
                # A literal \u... that is not a JSON unicode escape.
                out.append('\\\\u')
                fixes += 1
                i += 2
                continue

            # Invalid JSON escape: preserve the intended literal backslash.
            out.append('\\\\')
            out.append(nxt)
            fixes += 1
            i += 2
            continue

        # Raw control characters are illegal inside JSON strings.
        code = ord(ch)
        if code < 0x20:
            replacements = {
                '\n': '\\n',
                '\r': '\\r',
                '\t': '\\t',
                '\b': '\\b',
                '\f': '\\f',
            }
            out.append(replacements.get(ch, f"\\u{code:04x}"))
            fixes += 1
            i += 1
            continue

        out.append(ch)
        i += 1

    return ''.join(out), fixes


def stable_cell_id(path: Path, index: int, cell: dict[str, Any]) -> str:
    payload = f"{path.as_posix()}:{index}:{cell.get('cell_type','')}:{cell.get('source','')}"
    digest = hashlib.sha1(payload.encode('utf-8')).hexdigest()[:12]
    return f"cell-{index:03d}-{digest}"


def normalize_structure(data: dict[str, Any], path: Path) -> tuple[dict[str, Any], bool]:
    changed = False

    if not isinstance(data, dict):
        raise ValueError("top-level notebook object is not a JSON object")

    if "cells" not in data or not isinstance(data.get("cells"), list):
        data["cells"] = []
        changed = True

    if "metadata" not in data or not isinstance(data.get("metadata"), dict):
        data["metadata"] = {}
        changed = True

    nbformat_major = data.get("nbformat", 4)
    if not isinstance(nbformat_major, int):
        nbformat_major = 4
        changed = True
    data["nbformat"] = nbformat_major

    nbformat_minor = data.get("nbformat_minor", 5)
    if not isinstance(nbformat_minor, int):
        nbformat_minor = 5
        changed = True
    data["nbformat_minor"] = nbformat_minor

    # Convert older notebook formats to v4 if needed.
    if data["nbformat"] != 4:
        nb = nbformat.from_dict(data)
        nb = nbformat.convert(nb, 4)
        data = dict(nb)
        changed = True

    # Cell IDs are part of nbformat 4.5. Upgrade minor version and add stable IDs.
    if data.get("nbformat_minor", 0) < 5:
        data["nbformat_minor"] = 5
        changed = True

    normalized_cells: list[dict[str, Any]] = []
    for idx, original in enumerate(data["cells"]):
        if not isinstance(original, dict):
            raise ValueError(f"cell {idx} is not a JSON object")
        cell = dict(original)

        ctype = cell.get("cell_type")
        if ctype not in {"code", "markdown", "raw"}:
            raise ValueError(f"cell {idx} has unsupported cell_type={ctype!r}")

        if not isinstance(cell.get("metadata"), dict):
            cell["metadata"] = {}
            changed = True

        source = cell.get("source", "")
        if isinstance(source, list):
            if not all(isinstance(s, str) for s in source):
                cell["source"] = [str(s) for s in source]
                changed = True
        elif not isinstance(source, str):
            cell["source"] = str(source)
            changed = True

        if not isinstance(cell.get("id"), str) or not cell.get("id"):
            cell["id"] = stable_cell_id(path, idx, cell)
            changed = True

        if ctype == "code":
            if "execution_count" not in cell or not (
                cell["execution_count"] is None or isinstance(cell["execution_count"], int)
            ):
                cell["execution_count"] = None
                changed = True
            if not isinstance(cell.get("outputs"), list):
                cell["outputs"] = []
                changed = True
        else:
            # These fields are not part of markdown/raw cell schemas.
            if "execution_count" in cell:
                cell.pop("execution_count", None)
                changed = True
            if "outputs" in cell:
                cell.pop("outputs", None)
                changed = True

        normalized_cells.append(cell)

    data["cells"] = normalized_cells
    return data, changed


def load_and_repair(path: Path) -> tuple[dict[str, Any], bool, int, str | None]:
    raw = path.read_text(encoding="utf-8-sig")
    repaired = False
    escape_fixes = 0
    parse_error: str | None = None

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        parse_error = f"{exc.msg} (line {exc.lineno}, column {exc.colno})"
        candidate, escape_fixes = repair_json_text(raw)
        try:
            data = json.loads(candidate)
        except json.JSONDecodeError as exc2:
            raise ValueError(
                f"JSON remains invalid after automatic repair: {exc2.msg} "
                f"(line {exc2.lineno}, column {exc2.colno})"
            ) from exc2
        repaired = True

    data, structural_change = normalize_structure(data, path)
    repaired = repaired or structural_change

    nb = nbformat.from_dict(data)
    nbformat.validate(nb)
    return dict(nb), repaired, escape_fixes, parse_error


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="repair files in place")
    mode.add_argument("--check", action="store_true", help="validate only; fail if repair would be needed")
    parser.add_argument("--strict", action="store_true", help="fail if any notebook cannot be repaired/validated")
    args = parser.parse_args()

    notebooks = sorted(
        p for p in Path(".").rglob("*.ipynb")
        if ".ipynb_checkpoints" not in p.parts and ".git" not in p.parts
    )

    if not notebooks:
        print("No .ipynb files found.")
        return 0

    failures: list[tuple[Path, str]] = []
    needs_repair: list[Path] = []
    repaired_count = 0

    print(f"Auditing {len(notebooks)} notebook(s)...")
    for path in notebooks:
        try:
            nb, changed, escape_fixes, parse_error = load_and_repair(path)
            if changed:
                needs_repair.append(path)
                details = []
                if parse_error:
                    details.append(f"original JSON error: {parse_error}")
                if escape_fixes:
                    details.append(f"repaired escapes/control chars: {escape_fixes}")
                suffix = "; ".join(details) if details else "nbformat normalization"

                if args.write:
                    path.write_text(
                        json.dumps(nb, ensure_ascii=False, indent=1) + "\n",
                        encoding="utf-8",
                    )
                    # Re-read exactly what was written and validate again.
                    written = json.loads(path.read_text(encoding="utf-8"))
                    nbformat.validate(nbformat.from_dict(written))
                    repaired_count += 1
                    print(f"REPAIRED  {path}  [{suffix}]")
                else:
                    print(f"NEEDS FIX {path}  [{suffix}]")
            else:
                print(f"OK        {path}")
        except (ValueError, NotebookValidationError, UnicodeError) as exc:
            failures.append((path, str(exc)))
            print(f"FAILED    {path}: {exc}")

    print("\nSummary")
    print(f"  notebooks: {len(notebooks)}")
    print(f"  repaired/would repair: {len(needs_repair)}")
    print(f"  failed: {len(failures)}")

    if failures:
        print("\nUnrecoverable notebooks:")
        for path, message in failures:
            print(f"  - {path}: {message}")
        return 1 if args.strict else 0

    if args.check and needs_repair:
        return 1

    if args.write:
        print(f"  files written: {repaired_count}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
