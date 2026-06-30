# -*- coding: utf-8 -*-
"""
Idempotent setup script for the video-to-rpa-doc skill.

- Creates <skill_root>/env/ virtual environment if missing
- Installs/updates dependencies from requirements.txt
- Prints the absolute path to the venv python so callers can use it

Usage:
    python scripts/setup_env.py

Exit code 0 on success; non-zero on failure. Safe to run repeatedly.
"""
import os
import subprocess
import sys
import venv


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(SCRIPT_DIR)
ENV_DIR = os.path.join(SKILL_ROOT, "env")
REQUIREMENTS = os.path.join(SKILL_ROOT, "requirements.txt")


def venv_python_path():
    """Return the python.exe / python path inside the venv (regardless of OS)."""
    if os.name == "nt":
        return os.path.join(ENV_DIR, "Scripts", "python.exe")
    return os.path.join(ENV_DIR, "bin", "python")


def ensure_venv():
    py = venv_python_path()
    if os.path.exists(py):
        print(f"[ok] venv already exists: {ENV_DIR}")
        return py

    print(f"[..] creating venv at {ENV_DIR}")
    venv.EnvBuilder(with_pip=True, clear=False).create(ENV_DIR)
    print(f"[ok] venv created")
    return py


def install_requirements(py):
    if not os.path.exists(REQUIREMENTS):
        print(f"[warn] requirements.txt not found at {REQUIREMENTS}, skipping install")
        return

    print(f"[..] installing dependencies from {REQUIREMENTS}")
    cmd = [py, "-m", "pip", "install", "-r", REQUIREMENTS, "--disable-pip-version-check"]
    result = subprocess.run(cmd, capture_output=False)
    if result.returncode != 0:
        print(f"[err] pip install failed (exit {result.returncode})")
        sys.exit(result.returncode)
    print(f"[ok] dependencies installed")


def main():
    print(f"Skill root: {SKILL_ROOT}")
    py = ensure_venv()
    install_requirements(py)

    # Final line is parseable by callers: VENV_PYTHON=<abs path>
    print(f"VENV_PYTHON={py}")


if __name__ == "__main__":
    main()
