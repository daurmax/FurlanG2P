"""Ensure that the CLI entry point prints help."""

from __future__ import annotations

import shutil
import subprocess
import sys


def test_cli_help_runs() -> None:
    exe = shutil.which("furlang2p")
    cmd = (
        [exe, "--help"] if exe is not None else [sys.executable, "-m", "furlan_g2p.main", "--help"]
    )
    proc = subprocess.run(cmd, capture_output=True, text=True)
    assert proc.returncode == 0
    assert "FurlanG2P" in proc.stdout or "Usage" in proc.stdout
