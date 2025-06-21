import argparse
import csv
from tabulate import tabulate


def parse_where_condition(where_str):
    # Формат: column<operator>value, например price>500, name=iphone
    # Поддерживаем операторы >, <, =
    for op in ['>', '<', '=']:
        if op in where_str:
            parts = where_str.split(op, 1)
            if len(parts) == 2:
                column, value = parts
                return column.strip(), op, value.strip()
    raise ValueError(f"Invalid where condition: {where_str}")


def filter_rows(rows, column, operator, value):
    filtered = []
    for row in rows:
        cell = row[column]
        # Попытаемся сравнить численно, если возможно
        try:
            cell_val = float(cell)
            value_val = float(value)
        except ValueError:
            cell_val = cell
            value_val = value

        if operator == '>':
            if isinstance(cell_val, float) and isinstance(value_val, float):
                if cell_val > value_val:
                    filtered.append(row)
            else:
                # Для текстовых значений > - лексикографический порядок
                if cell_val > value_val:
                    filtered.append(row)
        elif operator == '<':
            if isinstance(cell_val, float) and isinstance(value_val, float):
                if cell_val < value_val:
                    filtered.append(row)
            else:
                if cell_val < value_val:
                    filtered.append(row)
        elif operator == '=':
            if cell_val == value_val:
                filtered.append(row)
        else:
            raise ValueError(f"Unsupported operator: {operator}")
    return filtered


def aggregate_rows(rows, operation, column):
    # Гарантируется, что column числовой
    values = [float(row[column]) for row in rows]
    if not values:
        return None
    if operation == 'avg':
        return sum(values) / len(values)
    elif operation == 'min':
        return min(values)
    elif operation == 'max':
        return max(values)
    else:
        raise ValueError(f"Unsupported aggregate operation: {operation}")


def parse_aggregate(aggregate_str):
    # Формат: operation=column, например avg=price
    parts = aggregate_str.split('=', 1)
    if len(parts) != 2:
        raise ValueError(f"Invalid aggregate argument: {aggregate_str}")
    operation, column = parts
    operation = operation.strip()
    column = column.strip()
    if operation not in ('avg', 'min', 'max'):
        raise ValueError(f"Unsupported aggregate operation: {operation}")
    return operation, column


def main():
    parser = argparse.ArgumentParser(
        description='CSV filter and aggregate tool')
    parser.add_argument('--file', required=True, help='Path to CSV file')
    parser.add_argument('--where', help='Filter condition, e.g. price>500')
    parser.add_argument('--aggregate', help='Aggregation, e.g. avg=price')

    args = parser.parse_args()

    with open(args.file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if args.where:
        column, operator, value = parse_where_condition(args.where)
        if column not in rows[0]:
            raise ValueError(f"Column '{column}' not found in CSV")
        rows = filter_rows(rows, column, operator, value)

    if args.aggregate:
        operation, column = parse_aggregate(args.aggregate)
        if column not in rows[0]:
            raise ValueError(f"Column '{column}' not found in CSV")
        result = aggregate_rows(rows, operation, column)
        if result is None:
            print("No data to aggregate")
        else:
            # Выводим в виде таблицы с заголовком
            print(tabulate([[operation, column, result]],
                           headers=['Operation', 'Column', 'Result']))
    else:
        if not rows:
            print("No data after filtering")
        else:
            print(tabulate(rows, headers="keys"))


if __name__ == '__main__':
    main()
