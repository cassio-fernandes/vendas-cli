import sys
from unittest.mock import patch, MagicMock

import pytest

from tests.fixtures.cli import cli_instance


def test_group_has_sale_command(cli_instance):
    # Arrange
    cli = cli_instance

    # Act / Assert
    assert cli is not None
    assert "read" in cli.commands


def test_command_without_arguments_prints_usage(cli_instance, capsys, monkeypatch):
    # Arrange
    cli = cli_instance
    monkeypatch.setattr(sys, "argv", ["prog"])

    # Act
    cli.__call__()

    # Assert
    captured = capsys.readouterr()
    assert "Uso:" in captured.out
    assert "Comandos disponíveis" in captured.out


def test_nonexistent_command_logs_error(cli_instance, monkeypatch):
    # Arrange
    cli = cli_instance
    monkeypatch.setattr(sys, "argv", ["prog", "no_such_command"])

    from core import cli as core_cli

    with patch.object(core_cli.logger, "error") as mock_error:
        # Act
        cli.__call__()

        # Assert
        mock_error.assert_called_once_with("Comando 'no_such_command' não encontrado.")
