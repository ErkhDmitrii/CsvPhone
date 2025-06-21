# CSV Filter and Aggregate Tool

Утилита для фильтрации и агрегации данных из CSV-файлов с удобным табличным выводом.

---

## Возможности

- Фильтрация строк по условию (`>`, `<`, `=`) для любого столбца
- Агрегация данных: среднее (`avg`), минимум (`min`), максимум (`max`)
- Вывод результатов в удобном табличном формате с помощью `tabulate`
- Простое использование через командную строку

---

## Установка

Рекомендуется использовать виртуальное окружение:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows


Установите зависимости:

pip install -r requirements.txt
Использование
python csv_tool.py --file path/to/file.csv [--where "column>value"] [--aggregate "operation=column"]
Примеры
Вывести весь CSV:

python csv_tool.py --file sample.csv
Отфильтровать товары с ценой больше 500:

python csv_tool.py --file sample.csv --where "price>500"
Посчитать среднюю цену:

python csv_tool.py --file sample.csv --aggregate "avg=price"
Отфильтровать по бренду Xiaomi и найти максимальный рейтинг:

python csv_tool.py --file sample.csv --where "brand=xiaomi" --aggregate "max=rating"
Запуск тестов
pytest
Пример CSV
name,brand,price,rating
iphone 15 pro,apple,999,4.9
galaxy s23 ultra,samsung,1199,4.8
redmi note 12,xiaomi,199,4.6
poco x5 pro,xiaomi,299,4.4
