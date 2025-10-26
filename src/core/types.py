from typing import Callable, List


class CommandType:
    hint: str
    func: Callable
    params: List[str]
