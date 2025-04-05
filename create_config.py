import json
import os

CONFIG_FILE = "config.json"


def create_or_load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            config = json.load(file)
            print("Конфигурация загружена из файла.")
    else:
        print("Файл конфигурации не найден. Посетите https://my.telegram.org/ и получите api_id и api_hash")
        config = {
            "api_id": int(input("Введите api_id: ")),
            "api_hash": input("Введите api_hash: ").strip(),
            "phone": input("Введите номер телефона в формате +1234567890: ").strip()
        }
        with open(CONFIG_FILE, "w", encoding="utf-8") as file:
            json.dump(config, file, indent=4, ensure_ascii=False)
            print("Конфигурация сохранена в файл.")

    return config
