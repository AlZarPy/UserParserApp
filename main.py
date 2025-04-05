import asyncio
import logging
import os
from create_config import create_or_load_config
from dialogs import get_all_channels
from users import parse_chat_users
from export import save_users_to_csv
from telethon.errors import SessionPasswordNeededError
from telethon.sync import TelegramClient

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def ask_for_load_chats():
    """Запросить у пользователя, хочет ли он загрузить доступные чаты."""
    print("Хотите загрузить список доступных чатов? Введите '1' для подтверждения или '0' для отмены.")
    user_input = input("Ваш выбор: ")

    if user_input == '1':
        return True
    elif user_input == '0':
        return False
    else:
        print("Некорректный ввод. Попробуйте снова.")
        return ask_for_load_chats()  # Рекурсивно запрашиваем, пока не получим правильный ввод

async def run_program():
    """Основная логика программы."""
    print("Загружаю конфигурацию...")
    config = create_or_load_config()

    api_id = config["api_id"]
    api_hash = config["api_hash"]
    phone = config["phone"]

    print("Инициализация клиента Telegram...")
    client = TelegramClient('session_name', api_id, api_hash)

    try:
        await client.start(phone)
    except SessionPasswordNeededError:
        print("Необходим двухфакторный пароль для доступа к аккаунту.")
        return

    # Предлагаем загрузить доступные чаты
    load_chats = ask_for_load_chats()

    channels = []
    if load_chats:
        print("Загружаю доступные каналы...")
        channels = await get_all_channels(client)

        if channels:
            print("Список доступных каналов:")
            for channel in channels:
                print(f"Статус: {channel['status']}, Название: {channel['name']}, ID: {channel['id']}, Username: {channel['username'] or 'Нет'}")
        else:
            print("Нет доступных каналов.")
    else:
        print("Вы выбрали не загружать каналы.")

    # Запрос от пользователя на ввод ID/username чата и дней
    chat = input("Введите ID или username чата: ").strip()
    days = int(input("За сколько дней парсить сообщения: ").strip())

    print("Собираю данные...")
    try:
        users = await parse_chat_users(client, chat, days)

        if users:
            filename = "user_data.csv"
            save_users_to_csv(users, filename=filename)
            file_path = os.path.abspath(filename)  # Получаем абсолютный путь к файлу
            print(f"Данные успешно собраны и сохранены в файл: {file_path}")
        else:
            print("Не удалось собрать данные. Проверьте правильность ID/username чата.")
    except Exception as e:
        print(f"Произошла ошибка при сборе данных: {e}")

def main():
    """Точка входа в программу."""
    asyncio.run(run_program())

if __name__ == "__main__":
    main()
    input("\nНажмите Enter, чтобы выйти...")
