import csv
import logging

logger = logging.getLogger(__name__)

def save_users_to_csv(users: list[dict], filename: str = 'user_data.csv'):
    fieldnames = ["name", "username", "about", "message_count", "last_message_date"]
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(users)
        logger.info(f"Данные успешно сохранены в файл '{filename}'")
    except Exception as e:
        logger.error(f"Ошибка при сохранении CSV: {e}")
