from pytest import fixture
import importlib
from core.cli import CliCommandGroup


@fixture
def cli_instance():
    importlib.import_module("core.commands.sales")

    cli = CliCommandGroup._CliCommandGroup__cli_instance
    return cli
