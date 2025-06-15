import argparse
import os
import sys
from footnotes import normalize_footnotes

def main():
    parser = argparse.ArgumentParser(description="📝 Нормализация сносок в Markdown-файле")
    parser.add_argument("input", help="✍️ Путь к входному файлу Markdown")
    parser.add_argument("output", help="📄 Путь к выходному файлу Markdown")
    args = parser.parse_args()

    try:
        print(f"\n📁 Чтение файла: {args.input}")
        with open(args.input, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ Ошибка: файл '{args.input}' не найден.")
        sys.exit(1)
    except Exception as e:
        print(f"⚠️ Ошибка при чтении файла: {e}")
        sys.exit(1)

    try:
        print("\n👨‍💻 Обработка содержимого...")
        updated = normalize_footnotes(content, verbose=True)
    except Exception as e:
        print(f"⚠️ Ошибка при обработке содержимого: {e}")
        sys.exit(1)

    try:
        print(f"\n✏️ Запись результата в файл: {args.output}")
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(updated)
        print(f"\n🎉 Готово! Файл сохранён: {args.output}")
    except Exception as e:
        print(f"⚠️ Ошибка при записи в файл: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
