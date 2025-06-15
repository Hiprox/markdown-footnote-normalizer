# Markdown Footnote Normalizer

Утилита для нормализации сносок в Markdown-файлах. Полезна при объединении нескольких документов с повторяющимися номерами сносок.

## Возможности

- Перенумеровывает сноски, исключая дублирование номеров.
- Объединяет дубликаты по содержимому.
- Удаляет старые определения сносок.
- Добавляет новые определения в конец файла.
- Убирает лишние пустые строки.
- Поддерживает запуск из командной строки.

## Пример

### Входной файл (`input.md`)

```markdown
Вот текст со сноской [^1] и ещё одной [^2].

[^1]: https://example.com/first

Другой раздел текста со сноской [^1].

[^1]: https://example.com/second
[^2]: https://example.com/second
```

### Выходной файл (`output.md`)

```markdown
Вот текст со сноской [^1] и ещё одной [^2].

Другой раздел текста со сноской [^3].

[^1]: https://example.com/first
[^2]: https://example.com/second
[^3]: https://example.com/second
```

> 🔄 Ссылки [^1] с разным содержимым были перенумерованы, а повторяющееся определение [^2] использовано повторно.

## Установка

> *Не поддерживается.*

## Использование

### Через CLI

> *Не поддерживается.*

### Через Python API

```python
from footnotes import normalize_footnotes

with open("input.md", encoding="utf-8") as f:
    content = f.read()

result = normalize_footnotes(content)
```

## Тесты

```bash
python -m unittest discover -s tests
```

## Требования

- Python 3.8+

## Лицензия

MIT License