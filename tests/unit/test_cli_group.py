import sys
from core.cli import CliGroup


def test_command_decorator_registers_command():
    # Arrange
    cli = CliGroup("testprog")

    # Act
    @cli.command(name="foo", hint="hint", params=["--a"]) # register command
    def foo():
        return "ok"

    # Assert
    assert "foo" in cli.commands
    cmd = cli.commands["foo"]
    assert cmd.hint == "hint"
    assert cmd.params == ["--a"]
    assert cmd.func is foo
