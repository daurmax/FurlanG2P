"""Tkinter-based graphical interface for the FurlanG2P pipeline."""

from __future__ import annotations

import argparse
import tkinter as tk
from collections.abc import Sequence
from tkinter import messagebox, ttk
from typing import Protocol

from furlan_g2p.services.pipeline import PipelineService


class MessageboxProtocol(Protocol):
    """Protocol describing the subset of :mod:`tkinter.messagebox` we use."""

    def showerror(self, title: str, message: str) -> None:  # pragma: no cover - Protocol
        """Display an error dialog."""


class UIController:
    """Orchestrate calls to :class:`~furlan_g2p.services.pipeline.PipelineService`.

    Parameters
    ----------
    pipeline:
        Optional pipeline instance.  Tests inject a mock implementation to
        validate the formatting logic without exercising the full pipeline.
    messagebox_module:
        Module exposing :func:`showerror`.  The default is
        :mod:`tkinter.messagebox`, but allowing injection keeps the controller
        deterministic during unit tests.

    Notes
    -----
    For very long texts the processing step could run in a worker thread and
    push results back to the UI via :meth:`tk.Misc.after`.  The current
    implementation is synchronous to keep the tool lightweight.
    """

    def __init__(
        self,
        pipeline: PipelineService | None = None,
        messagebox_module: MessageboxProtocol | None = None,
    ) -> None:
        self.pipeline = pipeline or PipelineService()
        self._messagebox = messagebox_module or messagebox

    def process(self, raw_text: str) -> str:
        """Process ``raw_text`` and return a formatted string for display.

        ``raw_text`` is left untouched so that the pipeline receives exactly
        what the user entered.  When the pipeline raises an exception the
        controller emits a non-blocking dialog and returns an empty string,
        allowing the UI layer to decide how to react.
        """

        if not raw_text.strip():
            return ""
        try:
            normalized, phonemes = self.pipeline.process_text(raw_text)
        except Exception as exc:
            self._messagebox.showerror(
                "Processing error",
                f"Unable to process the provided text. Details: {exc}",
            )
            return ""
        return self.format_output(normalized, phonemes)

    @staticmethod
    def format_output(normalized: str, phonemes: Sequence[str]) -> str:
        """Return the string shown in the output pane."""

        phoneme_text = " ".join(phonemes).strip()
        normalized_text = normalized.strip()

        sections: list[str] = []
        if normalized_text:
            sections.append(f"Normalized:\n{normalized}")
        elif normalized:
            sections.append(f"Normalized:\n{normalized}")
        if phoneme_text:
            sections.append(f"Phonemes:\n{phoneme_text}")
        return "\n\n".join(sections) if sections else ""


class _ReadOnlyText(tk.Text):
    """Text widget that disallows user edits while keeping selection enabled."""

    _NAVIGATION_KEYS = {
        "Left",
        "Right",
        "Up",
        "Down",
        "Home",
        "End",
        "Next",
        "Prior",
    }

    def __init__(self, master: tk.Misc, **kwargs: object) -> None:
        super().__init__(master, **kwargs)
        self.configure(cursor="arrow", wrap="word", undo=False, takefocus=True)
        self.bind("<Key>", self._on_keypress)
        self.bind("<<Paste>>", lambda _event: "break")
        self.bind("<<Cut>>", lambda _event: "break")
        self.bind("<Button-1>", self._focus_on_click)
        self.bind("<Button-2>", lambda _event: "break")
        self.bind("<Button-3>", self._focus_on_click)

    def _on_keypress(self, event: tk.Event) -> str | None:
        if event.keysym in self._NAVIGATION_KEYS:
            return None
        if event.keysym in {"Shift_L", "Shift_R", "Control_L", "Control_R"}:
            return None
        if event.keysym == "Insert" and event.state & 0x1:  # Shift pressed
            return "break"
        if event.state & 0x4:  # Control pressed
            lowered = event.keysym.lower()
            if lowered in {"c", "a"} or event.keysym == "Insert":
                return None
        if event.keysym in {"BackSpace", "Delete", "Return", "KP_Enter", "Tab", "space"}:
            return "break"
        if len(event.keysym) == 1:
            return "break"
        return None

    def _focus_on_click(self, event: tk.Event) -> None:
        self.focus_set()


class Application:
    """Build and manage the Tkinter user interface."""

    def __init__(self, root: tk.Tk, controller: UIController | None = None) -> None:
        self.root = root
        self.controller = controller or UIController()

        self.root.title("FurlanG2P — GUI")
        self.root.minsize(640, 480)
        self._style = ttk.Style(self.root)
        self._configure_style()
        self._build_layout()
        self._bind_events()
        self._update_process_state()
        self._update_copy_state()

    def _configure_style(self) -> None:
        """Apply a light modern theme."""

        theme = self._style.theme_use()
        if theme == "clam":
            return
        try:
            self._style.theme_use("clam")
        except tk.TclError:
            self._style.theme_use(theme)
        padding = {"padding": (8, 4)}
        self._style.configure("TButton", **padding)
        self._style.configure("TLabel", padding=(2, 2))

    def _build_layout(self) -> None:
        """Create widgets and arrange them using a responsive grid."""

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        main = ttk.Frame(self.root, padding=16)
        main.grid(row=0, column=0, sticky="nsew")
        main.columnconfigure(0, weight=1)
        main.columnconfigure(1, weight=0)
        main.rowconfigure(1, weight=1)
        main.rowconfigure(3, weight=1)

        ttk.Label(main, text="Input").grid(row=0, column=0, sticky="w")
        self.input_text = tk.Text(main, wrap="word", height=8, undo=True)
        self.input_text.grid(row=1, column=0, sticky="nsew", pady=(4, 12))
        self.input_text.configure(font=("TkDefaultFont", 11))
        input_scroll = ttk.Scrollbar(main, orient="vertical", command=self.input_text.yview)
        input_scroll.grid(row=1, column=1, sticky="ns", pady=(4, 12), padx=(8, 0))
        self.input_text.configure(yscrollcommand=input_scroll.set)

        ttk.Label(main, text="Output").grid(row=2, column=0, sticky="w")
        self.output_text = _ReadOnlyText(main, height=10)
        self.output_text.grid(row=3, column=0, sticky="nsew", pady=(4, 12))
        self.output_text.configure(font=("TkDefaultFont", 11))
        output_scroll = ttk.Scrollbar(main, orient="vertical", command=self.output_text.yview)
        output_scroll.grid(row=3, column=1, sticky="ns", pady=(4, 12), padx=(8, 0))
        self.output_text.configure(yscrollcommand=output_scroll.set)

        buttons = ttk.Frame(main)
        buttons.grid(row=4, column=0, columnspan=2, sticky="e")
        self.process_button = ttk.Button(buttons, text="Process", command=self.on_process)
        self.process_button.grid(row=0, column=0, padx=(0, 8))
        self.copy_button = ttk.Button(buttons, text="Copy output", command=self.on_copy_output)
        self.copy_button.grid(row=0, column=1)

    def _bind_events(self) -> None:
        """Wire up widget events."""

        self.input_text.bind("<<Modified>>", self._on_input_modified)
        self.input_text.bind("<Control-Return>", self.on_process)
        self.input_text.bind("<Control-KP_Enter>", self.on_process)
        self.root.bind_all("<Alt-c>", self.on_copy_output)
        self.root.bind_all("<Alt-C>", self.on_copy_output)

    def _on_input_modified(self, _event: tk.Event) -> None:
        self.input_text.edit_modified(False)
        self._update_process_state()

    def _update_process_state(self) -> None:
        raw = self.get_input_text().strip()
        if raw:
            self.process_button.state(["!disabled"])
        else:
            self.process_button.state(["disabled"])

    def _update_copy_state(self) -> None:
        if self.get_output_text():
            self.copy_button.state(["!disabled"])
        else:
            self.copy_button.state(["disabled"])

    def get_input_text(self) -> str:
        """Return the current input text without the trailing newline."""

        return self.input_text.get("1.0", tk.END).rstrip("\n")

    def get_output_text(self) -> str:
        """Return the rendered output text."""

        return self.output_text.get("1.0", tk.END).rstrip("\n")

    def set_output_text(self, text: str) -> None:
        """Replace the contents of the output widget."""

        self.output_text.delete("1.0", tk.END)
        if text:
            self.output_text.insert("1.0", text)
        self.output_text.see("1.0")

    def on_process(self, event: tk.Event | None = None) -> str | None:
        """Handle the "Process" action."""

        result = self.controller.process(self.get_input_text())
        self.set_output_text(result)
        self._update_copy_state()
        if event is not None:
            return "break"
        return None

    def on_copy_output(self, event: tk.Event | None = None) -> str | None:
        """Copy the entire output to the clipboard."""

        text = self.get_output_text()
        if not text:
            return "break" if event is not None else None
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update()
        if event is not None:
            return "break"
        return None


def run(argv: Sequence[str] | None = None) -> None:
    """Launch the Tkinter interface."""

    parser = argparse.ArgumentParser(
        prog="furlang2p ui",
        description=(
            "Launch the Tkinter interface to normalize text and view its phoneme "
            "sequence."
        ),
    )
    parser.add_argument(
        "--geometry",
        help="Optional Tk geometry string, for example 1024x768.",
    )
    args = parser.parse_args(argv if argv is not None else None)

    root = tk.Tk()
    if args.geometry:
        root.geometry(args.geometry)
    Application(root)
    root.mainloop()


if __name__ == "__main__":  # pragma: no cover - manual invocation helper
    run()
