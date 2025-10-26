from core.cli import CliCommandGroup
from parser.extract import Parser
from output.functions import get_sale_details, to_text, to_json
from core import logger


@CliCommandGroup.group(name="sales")
def sales():
    ...


@sales.command(name="read", params=["--start", "--end", "--format"], hint="ler arquivo .csv a partir de um diretório")
def cmd_read_csv(*args, format: str = "text", start: str|None = None, end: str|None = None):
    sales = Parser.read_csv(path=args[0])
    detail = get_sale_details(data=sales)
    
    match format:
        case "json":
            to_json(detail)
        case "text":
            to_text(detail)
        case _:
            logger.error(f"formato {format} não é válido")
