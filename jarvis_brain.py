import os

def FileReader(path="."):
    content = []
    try:
        for item in os.listdir(path):
            full_path = os.path.join(path, item)
            if os.path.isfile(full_path):
                content.append(f"Содержимое файла {item}:")
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        content.append(f.read())
                except Exception as e:
                    content.append(f"Не удалось прочитать файл: {e}")
    except Exception as e:
        return f"Ошибка при сканировании директории: {e}"
    return "\n".join(content)