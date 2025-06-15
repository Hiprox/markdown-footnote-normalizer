import unittest
from footnotes import normalize_footnotes


class TestNormalizeFootnotes(unittest.TestCase):
    # Проверяет, что сноска и её определение корректно обрабатываются, если они идут вместе
    def test_single_block(self):
        md = """
Текст с ссылкой [^1].

[^1]: Сноска первая
""".strip()
        expected = """
Текст с ссылкой [^1].

[^1]: Сноска первая
""".strip()
        self.assertEqual(normalize_footnotes(md), expected)

    # Проверяет, что одинаковые номера сносок в разных блоках получают разные номера
    def test_two_blocks_same_number(self):
        md = """
Текст A [^1].

[^1]: Сноска A

Другой текст B [^1].

[^1]: Сноска B
""".strip()
        expected = """
Текст A [^1].

Другой текст B [^2].

[^1]: Сноска A
[^2]: Сноска B
""".strip()
        self.assertEqual(normalize_footnotes(md), expected)

    # Проверяет, что одинаковые по содержимому сноски получают один и тот же новый номер
    def test_duplicate_footnote_content(self):
        md = """
Текст A [^1].

[^1]: Дублированная

Текст B [^1].

[^1]: Дублированная
""".strip()
        expected = """
Текст A [^1].

Текст B [^1].

[^1]: Дублированная
""".strip()
        self.assertEqual(normalize_footnotes(md), expected)

    # Проверяет, что если у ссылки нет определения — она остаётся как есть
    def test_no_definition(self):
        md = 'Текст без определения [^9].'.strip()
        expected = 'Текст без определения [^9].'.strip()
        self.assertEqual(normalize_footnotes(md), expected)

    # Проверяет, что дубликаты сносок устраняются, и не остаётся лишних \n между блоками
    def test_deduplicate_with_newlines(self):
        md = """
Текст A [^1].

[^1]: Одинаковый текст

Текст B [^2].

[^2]: Одинаковый текст
""".strip()

        expected = """
Текст A [^1].

Текст B [^1].

[^1]: Одинаковый текст
""".strip()

        result = normalize_footnotes(md)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()