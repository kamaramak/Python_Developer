def format_russian_text(data, count_1: str, count_234: str, count_other: str):
    if data % 10 == 1:
        return count_1
    elif data % 10 in (2, 3, 4):
        return count_234
    return count_other
