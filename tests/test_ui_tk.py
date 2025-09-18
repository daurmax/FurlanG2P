from __future__ import annotations

from collections.abc import Generator
from unittest.mock import Mock

import pytest

try:
    import tkinter as tk
except Exception:  # pragma: no cover - handled in fixture
    tk = None  # type: ignore[assignment]

from furlan_g2p.ui.tk_ui import Application


@pytest.fixture
def tk_root() -> Generator[tk.Tk, None, None]:
    if tk is None:
        pytest.skip("tkinter is not available")
    try:
        root = tk.Tk()
    except tk.TclError as exc:  # pragma: no cover - depends on CI
        pytest.skip(f"Tk cannot create a root window: {exc}")
    root.withdraw()
    yield root
    root.destroy()


def test_process_updates_output(tk_root: tk.Tk) -> None:
    controller = Mock()
    controller.process.return_value = "Normalized:\ncjase\n\nPhonemes:\nˈc a z e"
    app = Application(tk_root, controller=controller)

    app.input_text.insert("1.0", "Cjase")
    app.on_process()
    tk_root.update_idletasks()

    assert app.get_output_text() == "Normalized:\ncjase\n\nPhonemes:\nˈc a z e"
    controller.process.assert_called_once_with("Cjase")


def test_copy_button_uses_clipboard(tk_root: tk.Tk, monkeypatch: pytest.MonkeyPatch) -> None:
    controller = Mock()
    controller.process.return_value = "Normalized:\nfoo\n\nPhonemes:\nbar"
    app = Application(tk_root, controller=controller)
    app.input_text.insert("1.0", "foo")
    app.on_process()

    cleared = []
    appended: list[str] = []

    def fake_clear() -> None:
        cleared.append("clear")

    def fake_append(value: str) -> None:
        appended.append(value)

    monkeypatch.setattr(tk_root, "clipboard_clear", fake_clear)
    monkeypatch.setattr(tk_root, "clipboard_append", fake_append)
    monkeypatch.setattr(tk_root, "update", lambda: None)

    app.on_copy_output()

    assert cleared == ["clear"]
    assert appended == ["Normalized:\nfoo\n\nPhonemes:\nbar"]


def test_process_button_state_tracks_input(tk_root: tk.Tk) -> None:
    controller = Mock()
    app = Application(tk_root, controller=controller)

    assert "disabled" in app.process_button.state()

    app.input_text.insert("1.0", "ciao")
    app.input_text.event_generate("<<Modified>>")
    tk_root.update_idletasks()

    assert "disabled" not in app.process_button.state()

    app.input_text.delete("1.0", tk.END)
    app.input_text.event_generate("<<Modified>>")
    tk_root.update_idletasks()

    assert "disabled" in app.process_button.state()
