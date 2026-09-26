"""Order §7: engine/ must stay pure Python — no django / rest_framework imports.

Cheap static guard protecting the phase-2 Telegram reuse (backend/README.md).
The second test proves the guard has teeth (it detects a planted violation).
"""

import pathlib

BACKEND_ROOT = pathlib.Path(__file__).resolve().parent.parent
ENGINE_ROOT = BACKEND_ROOT / "engine"

FORBIDDEN = ("import django", "from django", "rest_framework")


def find_forbidden_imports(root: pathlib.Path) -> list[str]:
    offenders: list[str] = []
    for path in sorted(root.rglob("*.py")):
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if any(marker in line for marker in FORBIDDEN):
                offenders.append(f"{path.relative_to(root)}:{lineno}: {stripped}")
    return offenders


def test_engine_package_exists_and_is_import_free():
    assert ENGINE_ROOT.is_dir(), "backend/engine/ package is part of the T-001 layout"

    offenders = find_forbidden_imports(ENGINE_ROOT)
    assert not offenders, (
        "engine/ must never import django/rest_framework:\n" + "\n".join(offenders)
    )


def test_guard_detects_violations(tmp_path):
    (tmp_path / "impure.py").write_text(
        "from django.db import models  # planted violation\n", encoding="utf-8"
    )

    offenders = find_forbidden_imports(tmp_path)

    assert len(offenders) == 1
    assert "impure.py:1" in offenders[0]


def test_engine_has_no_non_python_strays():
    strays = [p.name for p in ENGINE_ROOT.rglob("*") if p.is_file() and p.suffix != ".py"]
    assert not strays, f"engine/ should hold only .py files, found: {strays}"
