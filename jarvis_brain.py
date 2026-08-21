import os
import shutil

def FileReader(path="."):
    """Чтение файлов в указанной директории"""
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

def CreateFile(filename, content):
    """
    Создаёт новый файл или перезаписывает существующий.
    """
    try:
        dir_name = os.path.dirname(filename)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Файл '{filename}' успешно создан/перезаписан."
    except Exception as e:
        return f"Ошибка при создании файла: {e}"

def EditFile(filename, old_text, new_text):
    """
    Заменяет первое вхождение old_text на new_text в файле filename.
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
        if old_text not in content:
            return f"Текст '{old_text}' не найден в файле '{filename}'."
        updated_content = content.replace(old_text, new_text, 1)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(updated_content)
        return f"Файл '{filename}' обновлён: первое вхождение '{old_text}' заменено."
    except Exception as e:
        return f"Ошибка при редактировании файла: {e}"

def CreateFolder(path):
    """
    Создаёт папку
    """
    try:
        os.makedirs(path, exist_ok=True)
        return f"Папка '{path}' успешно создана (или уже существовала)."
    except Exception as e:
        return f"Ошибка при создании папки: {e}"

def DeleteFile(path):
    """
    Удаляет файл по указанному пути.
    """
    try:
        if os.path.exists(path):
            os.remove(path)
            return f"Файл '{path}' успешно удалён."
        else:
            return f"Файл '{path}' не найден."
    except Exception as e:
        return f"Ошибка при удалении файла: {e}"


def DeleteFolder(path):
    """
    Удаляет папку со всем её содержимым.
    """
    try:
        if os.path.exists(path):
            shutil.rmtree(path)
            return f"Папка '{path}' успешно удалена вместе с содержимым."
        else:
            return f"Папка '{path}' не найдена."
    except Exception as e:
        return f"Ошибка при удалении папки: {e}"