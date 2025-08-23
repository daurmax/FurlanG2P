"""File I/O helpers (skeleton)."""

from __future__ import annotations


class IOService:
    """File I/O helpers (skeleton)."""

    def read_text(self, path: str) -> str:
        """Read text from ``path``."""
        raise NotImplementedError("read_text is not implemented yet.")

    def write_text(self, path: str, data: str) -> None:
        """Write ``data`` to ``path``."""
        raise NotImplementedError("write_text is not implemented yet.")


__all__ = ["IOService"]
