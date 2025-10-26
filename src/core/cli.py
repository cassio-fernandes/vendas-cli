import argparse
import sys
from typing import Callable, Dict, List, Tuple

from .types import CommandType
from . import logger


class CliGroup:

    def __init__(self, name: str):
        self.name = name
        self.commands: Dict[str, CommandType] = {}
        self.group_commands: Dict[str, list] = {}

    def _command_has_args(self) -> bool:
        if len(sys.argv) < 2:
            msg = f"""Uso: {self.name} <comando> [args...]
                \nComandos disponíveis:
            """
            print(msg)
            [print(f"- {name}: {args.hint}") for name, args in self.commands.items()]
   
            return False
        
        return True
    
    def _command_exists(self, cmd: str) -> Tuple[CommandType|None, bool]:
        _command: CommandType = self.commands.get(cmd)

        if not _command:
            logger.error(f"Comando '{cmd}' não encontrado.")
            return None, False
        
        return _command, True
    
    def _parse_arguments(self, cmd: CommandType) -> Tuple:
        sys.argv = sys.argv[2:]
        
        parser = argparse.ArgumentParser()
        [parser.add_argument(param, action="store") for param in cmd.params]
        
        return sys.argv, parser.parse_args()

    def command(self, name: str | None = None, hint: str = "", params: List[str] | None = None) -> Callable:
        def wrapper(func: Callable) -> Callable:
            cmd = name or func.__name__

            if cmd not in self.commands:
                self.commands[cmd] = CommandType()

            command = self.commands[cmd]
            command.func = func
            command.hint = hint
            command.params = params

            return func
        return wrapper
    
    def __call__(self):
        if not self._command_has_args():
            return
        
        _command_name = sys.argv[1]
        _command, exists = self._command_exists(cmd=_command_name)
        
        if not exists:
            return
        
        args, kwargs = self._parse_arguments(cmd=_command)
        
        _command.func(*args, kwargs)


class CliCommandGroup:

    __cli_instance: CliGroup|None = None

    @classmethod
    def group(cls, name: str):
        def wrapper(func: Callable):
            cls.__cli_instance = CliGroup(func.__name__)
            if name not in cls.__cli_instance.group_commands:
                cls.__cli_instance.group_commands[name] = list()
            
            cls.__cli_instance.group_commands[name] = cls.__cli_instance.commands
            func.__call__()
            
            return cls.__cli_instance
        return wrapper
    
    @classmethod
    def run(cls):
        try:
            cls.__cli_instance.__call__()
        except Exception as ex:
            logger.error(f"Erro ao executar comando: {ex}")
