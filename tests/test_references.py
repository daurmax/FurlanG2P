"""Tests for presence of bibliographic references."""

from pathlib import Path


def test_references_file_exists() -> None:
    """`docs/references.md` should exist."""
    assert Path("docs/references.md").is_file()


def test_readme_links_references() -> None:
    """Ensure the README links to the references file."""
    readme = Path("README.md").read_text(encoding="utf-8")
    assert "docs/references.md" in readme


def test_references_contains_key_sources() -> None:
    """The references list should include core sources."""
    refs = Path("docs/references.md").read_text(encoding="utf-8")
    assert "ARLeF" in refs and "Miotti" in refs
