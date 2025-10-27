from core.cli import CliCommandGroup
import importlib

importlib.import_module("core.commands.sales")

if __name__ == "__main__":
    CliCommandGroup.run()
