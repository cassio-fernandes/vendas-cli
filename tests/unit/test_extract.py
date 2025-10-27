import csv
from unittest.mock import patch

import pytest

from tests.fixtures.parser import valid_data, write_csv_file
from parser.extract import Parser


def test_parse_obj_returns_sales(valid_data):
    # Arrange
    row = valid_data[0]

    # Act
    sales = Parser._parse_obj(data=row)

    # Assert
    assert sales is not None
    assert getattr(sales, "product") == row["produto"]
    assert getattr(sales, "quantity") == int(row["quantidade"])
    assert getattr(sales, "price") == float(row["preco_unitario"])


def test_parser_should_raises_file_not_found(valid_data, tmp_path, write_csv_file):
    # Arrange
    csv_path = tmp_path / "missing.csv"
    write_csv_file(csv_path, valid_data)

    with patch.object(Parser, "_validate", side_effect=FileNotFoundError("Arquivo não encontrado")) as mock_validate:
        # Act
        result = Parser.read_csv(str(csv_path))

        # Assert
        mock_validate.assert_called_once()
        assert result == []


def test_read_csv_should_raises_value_error(valid_data, tmp_path, write_csv_file):
    # Arrange
    csv_path = tmp_path / "invalid_ext.txt"
    write_csv_file(csv_path, valid_data)

    with patch.object(Parser, "_validate", side_effect=ValueError("Arquivo inválido")) as mock_validate:
        # Act
        result = Parser.read_csv(str(csv_path))

        # Assert
        mock_validate.assert_called_once()
        assert result == []


def test_read_csv_is_resilient_when_unicode_error(tmp_path, write_csv_file):
    # Arrange
    csv_path = tmp_path / "latin1.csv"
    rows = [
        {"produto": "Tênis", "quantidade": "1", "preco_unitario": "199.9"},
    ]
    write_csv_file(csv_path, rows, encoding="latin-1")
    
    expected_price = 199.9
    expected_quantity = 1
    expected_product = "Tênis"

    # Act
    result = Parser.read_csv(str(csv_path))

    # Assert
    assert isinstance(result, list)
    assert len(result) == 1
    item = result[0]
    
    assert item.product == expected_product
    assert item.quantity == expected_quantity
    assert item.price == expected_price


def test_read_csv_handles_generic_exception(tmp_path, valid_data, write_csv_file):
    # Arrange
    csv_path = tmp_path / "some.csv"
    write_csv_file(csv_path, valid_data)

    with patch.object(Parser, "_validate", side_effect=Exception("boom")) as mock_validate:
        # Act
        result = Parser.read_csv(str(csv_path))

        # Assert
        mock_validate.assert_called_once()
        assert result == []


def test_read_csv_missing_column_should_returns_none_product(tmp_path, write_csv_file):
    # Arrange
    csv_path = tmp_path / "missing_produto.csv"
    content = "quantidade,preco_unitario\n2,10.0\n"
    csv_path.write_text(content, encoding="utf-8")

    # Act
    with patch.object(Parser, "_validate") as mock_validate:
        result = Parser.read_csv(str(csv_path))

        # Assert
        mock_validate.assert_called_once()
        assert isinstance(result, list)
        assert len(result) == 1
        item = result[0]
        assert item.product is None
        assert item.quantity == 2
        assert item.price == 10.0


def test_read_csv_with_extra_column_is_ignored(tmp_path):
    # Arrange
    csv_path = tmp_path / "extra_col.csv"
    content = "produto,quantidade,preco_unitario,extra-col\nCamiseta,3,49.9,ignored\n"
    csv_path.write_text(content, encoding="utf-8")

    # Act
    with patch.object(Parser, "_validate") as mock_validate:
        result = Parser.read_csv(str(csv_path))

        # Assert
        mock_validate.assert_called_once()
        assert isinstance(result, list)
        assert len(result) == 1
