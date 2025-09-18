from __future__ import annotations

from unittest.mock import Mock

import pytest

from furlan_g2p.ui.tk_ui import UIController


@pytest.fixture
def controller_with_mocks() -> tuple[UIController, Mock, Mock]:
    pipeline = Mock()
    messagebox = Mock()
    controller = UIController(pipeline=pipeline, messagebox_module=messagebox)
    return controller, pipeline, messagebox


def test_process_formats_output(controller_with_mocks: tuple[UIController, Mock, Mock]) -> None:
    controller, pipeline, messagebox = controller_with_mocks
    pipeline.process_text.return_value = ("cjase", ["ˈc", "a", "z", "e"])

    result = controller.process("Cjase")

    pipeline.process_text.assert_called_once_with("Cjase")
    assert result == "Normalized:\ncjase\n\nPhonemes:\nˈc a z e"
    messagebox.showerror.assert_not_called()


def test_process_ignores_empty_input(
    controller_with_mocks: tuple[UIController, Mock, Mock],
) -> None:
    controller, pipeline, messagebox = controller_with_mocks

    result = controller.process("   \n\t")

    assert result == ""
    pipeline.process_text.assert_not_called()
    messagebox.showerror.assert_not_called()


def test_process_reports_errors(controller_with_mocks: tuple[UIController, Mock, Mock]) -> None:
    controller, pipeline, messagebox = controller_with_mocks
    pipeline.process_text.side_effect = RuntimeError("boom")

    result = controller.process("ciao")

    assert result == ""
    messagebox.showerror.assert_called_once()
