import importlib
from unittest.mock import patch
from contextlib import ExitStack

import pytest


def test_cmd_read_csv_handle_format_param_sucessfully():
    # Arrange
    sales_mod = importlib.import_module("core.commands.sales")

    with ExitStack() as stack:
        mock_read = stack.enter_context(patch("core.commands.sales.Parser.read_csv", return_value=[]))
        mock_details = stack.enter_context(patch("core.commands.sales.get_sale_details", return_value={}))
        mock_to_json = stack.enter_context(patch("core.commands.sales.to_json"))
        mock_to_text = stack.enter_context(patch("core.commands.sales.to_text"))
        mock_error = stack.enter_context(patch("core.commands.sales.logger.error"))

        # Act
        sales_mod.cmd_read_csv("/tmp/fake.csv", format="json")
        sales_mod.cmd_read_csv("/tmp/fake.csv", format="text")

        # Assert
        mock_read.assert_called()
        mock_details.assert_called()
        mock_to_json.assert_called_once()
        mock_to_text.assert_called_once()

def test_cmd_read_csv_logs_error_on_invalid_format():
    # Arrange
    sales_mod = importlib.import_module("core.commands.sales")

    with ExitStack() as stack:
        mock_error = stack.enter_context(patch("core.commands.sales.logger.error"))

        # Act
        sales_mod.cmd_read_csv("/tmp/fake.csv", format="badfmt")

        # Assert invalid format logged
        mock_error.assert_called_with("formato badfmt não é válido")
