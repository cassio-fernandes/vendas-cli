import json
from unittest.mock import patch

import pytest

from output.functions import get_sale_details, to_json, to_text
from tests.fixtures.parser import sales_records, valid_data


def test_get_sale_details_success(sales_records):
    # Arrange
    data = sales_records

    # Act
    result = get_sale_details(data)
    sale_by_products = result["sale_by_products"]

    # Assert
    assert isinstance(result, dict)
    assert sale_by_products["Camiseta"] == 4
    assert sale_by_products["Calça"] == 2
    assert sale_by_products["Tênis"] == 1
    assert pytest.approx(result["total_sales"]) == pytest.approx(399.6)
    assert result["bestseller"] == "Camiseta"


def test_should_display_as_json(capsys):
    # Arrange
    data = {"a": 1}

    with patch("output.functions.json.dumps") as mock_dumps:
        mock_dumps.return_value = "JSON_STR"

        # Act
        to_json(data)

        # Assert
        mock_dumps.assert_called_once_with(data, indent=4, ensure_ascii=False)
        captured = capsys.readouterr()
        assert "JSON_STR" in captured.out
