from pytest import fixture
import csv
from parser.schema import Sales


@fixture
def valid_data():
    return [
        {"produto": "Camiseta", "quantidade": "3", "preco_unitario": "49.9"},
        {"produto": "Calça", "quantidade": "2", "preco_unitario": "99.9"},
        {"produto": "Camiseta", "quantidade": "1", "preco_unitario": "49.9"},
        {"produto": "Tênis", "quantidade": "1", "preco_unitario": "199.9"},
    ]


@fixture
def write_csv_file(tmp_path):
    def _write(path, rows, encoding: str = "utf-8"):
        headers = ["produto", "quantidade", "preco_unitario"]
        with open(path, "w", encoding=encoding, newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)

    return _write


@fixture
def sales_records(valid_data):
    records = []
    for data in valid_data:
        s = Sales()
        s.product = data["produto"]
        s.quantity = int(data.get("quantidade", 0))
        s.price = float(data.get("preco_unitario", 0.0))
        
        records.append(s)

    return records
