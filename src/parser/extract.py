import csv
from pathlib import Path
from typing import Dict, List
from core import logger
from parser.schema import Sales


class Parser:
    _file_path: str
    _file_extension: str
    _reader: csv.DictReader
    
    @classmethod
    def read_csv(cls, path: str, filter: bool = False) -> List[Dict[str, str]]:
        cls._file_path = Path(path).expanduser()
        _data: List[Dict] = []
        
        try:
            cls._validate()
            
            with cls._file_path.open(mode='r', encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    _parsed_obj = cls._parse_obj(data=row)
                    if _parsed_obj is not None:
                        _data.append(_parsed_obj)

        except UnicodeDecodeError:
            with cls._file_path.open(mode='r', encoding="latin-1", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    _parsed_obj = cls._parse_obj(data=row)
                    if _parsed_obj is not None:
                        _data.append(_parsed_obj)

        except FileNotFoundError as ex:
            logger.error(f"Falha ao processar o arquivo csv: {ex}")
        
        except ValueError as ex:
            logger.error(f"Falha ao processar o arquivo csv: {ex}")

        except Exception as ex:
            logger.error(f"Erro desconhecido: {ex}")

        return _data

    def _parse_obj(data: Dict) -> Sales|None:
        _valid_columns = ("produto", "quantidade", "preco_unitario")
        sales = Sales()

        if not all(col in data.keys() for col in _valid_columns):
            logger.error(f"colunas obrigatórias não encontradas {data.keys()}")
            return
        
        try:
            sales.product = data.get("produto")
            sales.quantity=int(data.get("quantidade"))
            sales.price=float(data.get("preco_unitario"))

            return sales
        
        except Exception as ex:
            logger.error(f"erro ao ler registros: {ex}")
            return

    @classmethod
    def _validate(cls):
        if not cls._file_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {cls._file_path}")
        
        if cls._file_path.suffix.lower() != ".csv":
            raise ValueError(f"O arquivo '{cls._file_path.name}' não é um CSV válido.")
