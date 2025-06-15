import re
from collections import OrderedDict

def normalize_footnotes(markdown: str, verbose: bool = False) -> str:
    """
    Нормализует сноски в Markdown-тексте.

    Выполняет следующие действия:
    - Перенумеровывает сноски по порядку с учётом контекста появления и размещения определений.
    - Удаляет старые определения сносок.
    - Исключает дубликаты определений (по тексту).
    - Удаляет подряд идущие пустые строки (оставляет не более одной).
    - Вставляет новые уникальные определения сносок в конец документа.

    Аргументы:
        markdown (str): Исходный Markdown-текст.
        verbose (bool): Флаг вывода отладочной информации.

    Возвращает:
        str: Обновлённый Markdown-документ с нормализованными сносками.
    """
    
    # Разделяем текст на строки
    lines = markdown.splitlines()
    new_refs = []  # список ссылок: (строка, позиция_начала, позиция_конца, старый_номер)
    definitions = []  # список определений: (строка, номер, текст)
    def_map = {}  # карта определений по позиции и номеру
    new_index = 1  # глобальный счётчик новых номеров сносок

    # Функция логирования, работает только если verbose=True
    def log(msg):
        if verbose:
            print(msg)

    log("\nНачало анализа документа...")

    # Первый проход: собираем все определения и ссылки
    for i, line in enumerate(lines):
        def_match = re.match(r"^\[\^(\d+)\]:\s*(.+)$", line)
        if def_match:
            num, text = def_match.groups()
            definitions.append((i, num, text))
            def_map[(i, num)] = text
            log(f"Обнаружено определение: строка {i}, номер {num}, текст: {text[:30]}...")
            continue

        # Поиск всех ссылок в строке
        for match in re.finditer(r"\[\^(\d+)\]", line):
            num = match.group(1)
            new_refs.append((i, match.start(), match.end(), num))

    log("\nСопоставление ссылок с определениями...")
    assignment = []  # список новых назначений: (новый_номер, текст_сноски)
    text_to_num = {}  # сопоставление текста сноски -> новый номер
    duplicate_count = 0
    usage_map = {}  # (позиция_ссылки) -> новый номер

    # Обрабатываем каждую ссылку, ищем соответствующее определение ниже
    for i, start, end, old_n in new_refs:
        candidates = [(j, n, t) for j, n, t in definitions if n == old_n and j > i]
        if not candidates:
            log(f"  Пропущена ссылка [^{old_n}] на строке {i}: определение не найдено")
            continue
        j, _, text = candidates[0]
        if text in text_to_num:
            new_n = text_to_num[text]
            duplicate_count += 1
        else:
            new_n = new_index
            text_to_num[text] = new_index
            new_index += 1
        usage_map[(i, start, end)] = new_n
        assignment.append((new_n, text))
        log(f"  Строка {i}: [^{old_n}] → [^{new_n}], определение на строке {j}")

    log("\nЗамена ссылок в тексте...")
    # Заменяем старые номера ссылок на новые в тексте
    for (i, start, end), new_n in sorted(usage_map.items(), reverse=True):
        line = lines[i]
        old = line[start:end]
        lines[i] = line[:start] + f"[^{new_n}]" + line[end:]
        log(f"  Строка {i}: заменено '{old}' на '[^{new_n}]'")

    log("\nУдаление старых определений...")
    # Удаляем строки, содержащие определения старых сносок
    new_lines = []
    for line in lines:
        if not re.match(r"^\[\^(\d+)\]:\s*(.+)$", line):
            new_lines.append(line)
    lines = new_lines

    log("\nФормирование новых определений...")
    seen = set()
    unique_defs = OrderedDict()
    # Убираем дубликаты определений по тексту
    for num, text in assignment:
        if text not in seen:
            unique_defs[num] = text
            seen.add(text)

    # Удаляем подряд идущие пустые строки (оставляем максимум одну)
    compacted = []
    previous_empty = False
    for line in lines:
        if line.strip() == "":
            if not previous_empty:
                compacted.append("")
            previous_empty = True
        else:
            compacted.append(line)
            previous_empty = False
    lines = compacted

    # Добавляем новые определения в конец, если они есть
    if unique_defs:
        if lines and lines[-1].strip() != "":
            lines.append("")
        for num, text in unique_defs.items():
            lines.append(f"[^{num}]: {text}")
            log(f"  [^{num}]: {text[:40]}...")

    log(f"\nУстранено дубликатов сносок: {duplicate_count}")
    return "\n".join(lines).strip()