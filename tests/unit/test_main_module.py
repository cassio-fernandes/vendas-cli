import runpy
from unittest.mock import patch


def test_main_executes_import_and_runs_cli(monkeypatch, tmp_path):
    main_path = "src/main.py"

    with patch("importlib.import_module") as mock_import, \
         patch("core.cli.CliCommandGroup.run"):
        # Act
        runpy.run_path(main_path, run_name="__main__")

        # Assert
        mock_import.assert_called_with("core.commands.sales")
