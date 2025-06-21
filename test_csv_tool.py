import csv_tool
import pytest


@pytest.fixture
def sample_rows():
    return [
        {'name':
         'iphone 15 pro', 'brand': 'apple', 'price': '999', 'rating': '4.9'},
        {'name':
         'galaxy s23 ultra',
         'brand': 'samsung', 'price': '1199', 'rating': '4.8'},
        {'name':
         'redmi note 12', 'brand': 'xiaomi', 'price': '199', 'rating': '4.6'},
        {'name':
         'poco x5 pro', 'brand': 'xiaomi', 'price': '299', 'rating': '4.4'},
    ]


@pytest.mark.parametrize("where_str, expected", [
    ("price>500", ['iphone 15 pro', 'galaxy s23 ultra']),
    ("brand=apple", ['iphone 15 pro']),
    ("rating<4.7", ['redmi note 12', 'poco x5 pro']),
])
def test_filter_rows(sample_rows, where_str, expected):
    column, operator, value = csv_tool.parse_where_condition(where_str)
    filtered = csv_tool.filter_rows(sample_rows, column, operator, value)
    names = [r['name'] for r in filtered]
    assert names == expected


@pytest.mark.parametrize("aggregate_str, expected", [
    ("avg=price", (999 + 1199 + 199 + 299) / 4),
    ("min=price", 199),
    ("max=price", 1199),
    ("avg=rating", (4.9 + 4.8 + 4.6 + 4.4) / 4),
])
def test_aggregate_rows(sample_rows, aggregate_str, expected):
    operation, column = csv_tool.parse_aggregate(aggregate_str)
    result = csv_tool.aggregate_rows(sample_rows, operation, column)
    assert abs(result - expected) < 1e-6


def test_parse_where_condition():
    assert csv_tool.parse_where_condition("price>100") == ('price', '>', '100')
    assert csv_tool.parse_where_condition("brand=apple") == (
        'brand', '=', 'apple')
    assert csv_tool.parse_where_condition("rating<4.5") == (
        'rating', '<', '4.5')
    with pytest.raises(ValueError):
        csv_tool.parse_where_condition("invalidcondition")


def test_parse_aggregate():
    assert csv_tool.parse_aggregate("avg=price") == ('avg', 'price')
    assert csv_tool.parse_aggregate("min=rating") == ('min', 'rating')
    with pytest.raises(ValueError):
        csv_tool.parse_aggregate("sum=price")
    with pytest.raises(ValueError):
        csv_tool.parse_aggregate("invalidformat")
