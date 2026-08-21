# Описание инструмента для модели
tools = [
    {
        "type": "function",
        "function": {
            "name": "websearch",
            "description": "Ищет информацию в интернете по заданному запросу. Используй, когда нужны актуальные данные или факты, которых нет в твоей памяти.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Поисковый запрос"},
                    "max_results": {"type": "integer", "description": "Количество результатов", "default": 3}
                },
                "required": ["query"]
            }
        }
    },
    {
            "type": "function",
            "function": {
                "name": "FileReader",
                "description": "Читает содержимое файлов в указанной директории (по умолчанию текущая). Позволяет просмотреть свой собственный код или любые локальные файлы для самоанализа.",
                "parameters": {
                    "type": "object",
                    "properties": {
                    "path": {
                        "type": "string",
                        "description": "Путь к директории, которую нужно просканировать. По умолчанию '.'",
                        "default": "."
                    }
                },
                    "required": []
                }
            }
    },
    {
    "type": "function",
    "function": {
        "name": "CreateFile",
        "description": "Создаёт новый файл или перезаписывает существующий. Используй, когда нужно сохранить код, заметку или любой другой текст в файл. Не используй этот инструмент, если не просили его использовать.",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "Путь к файлу (например, 'notes.txt' или 'src/utils.py')"
                },
                "content": {
                    "type": "string",
                    "description": "Полное содержимое файла"
                    }
                },
            "required": ["filename", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "EditFile",
            "description": "Заменяет первое вхождение указанного текста в файле на новый текст. Используй для точечного изменения кода или документа, не переписывая весь файл. Не используй этот инструмент, если не просили его использовать.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Путь к файлу"
                    },
                    "old_text": {
                        "type": "string",
                        "description": "Фрагмент текста, который нужно заменить"
                    },
                    "new_text": {
                        "type": "string",
                        "description": "Новый текст для замены"
                    }
                },
                "required": ["filename", "old_text", "new_text"]
            }
        }
    },
    {
    "type": "function",
    "function": {
        "name": "CreateFolder",
        "description": "Создаёт папку по указанному пути. Если промежуточные папки отсутствуют, они будут созданы автоматически.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Путь к папке (например, 'data/results' или 'new_folder')"
                    }
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "DeleteFile",
            "description": "Удаляет файл по указанному пути. Используй, когда нужно удалить ненужный файл.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Путь к файлу"
                    }
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "DeleteFolder",
            "description": "Удаляет папку и всё её содержимое без возможности восстановления. Используй с осторожностью.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Путь к папке"
                    }
                },
                "required": ["path"]
            }
        }
    }
]