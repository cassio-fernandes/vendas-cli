import json
from typing import Dict, List

from tabulate import tabulate

from parser.schema import Sales


def get_sale_details(data: List[Sales]) -> Dict:
    _total_product: Dict[str, float] = {}
    _total_sales: float = 0.0
    _bestseller: str|None = None

    for d in data:
        if d.product not in _total_product:
            _total_product[d.product] = 0
        _total_product[d.product] += d.quantity
        _total_sales += d.price
    
    _sorted_products = sorted(_total_product.items(), key = lambda item: item[1], reverse=True)
    
    if _sorted_products:
        _bestseller, _ = _sorted_products[0]

    return {
        "sale_by_products": _total_product,
        "total_sales": _total_sales,
        "bestseller": _bestseller
    }


def to_json(data: Dict):
    print(json.dumps(data, indent=4, ensure_ascii=False))


def to_text(data: Dict):
    rows = [{"Produto": k, "Quantidade": v} for k, v in data["sale_by_products"].items()]
    print("\n")
    print(tabulate(rows, headers="keys", tablefmt="github"))
    print(f"\nTotal de vendas: {data.get('total_sales')}")
    print(f"Produto mais vendido: {data.get('bestseller')}\n")
