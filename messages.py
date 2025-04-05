import logging
from datetime import datetime, timedelta
from collections import defaultdict

logger = logging.getLogger(__name__)

async def collect_users_from_chat(client, chat_id_or_username: str, days: int = 30):
    user_stats = defaultdict(lambda: {"count": 0, "last_message": None})
    offset_date = datetime.now() - timedelta(days=days)

    try:
        async for message in client.iter_messages(chat_id_or_username):
            msg_date = message.date.replace(tzinfo=None)

            if msg_date < offset_date:
                break  # Сообщение слишком старое — завершаем сбор

            if message.fwd_from:
                continue  # Пропускаем пересланные

            if not message.sender_id:
                continue  # Пропускаем системные

            user_id = message.sender_id
            user_stats[user_id]["count"] += 1

            if not user_stats[user_id]["last_message"] or msg_date > user_stats[user_id]["last_message"]:
                user_stats[user_id]["last_message"] = msg_date

        return user_stats
    except Exception as e:
        logger.error(f"Ошибка при сборе сообщений из чата {chat_id_or_username}: {e}")
        return {}