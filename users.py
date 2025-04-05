import logging
from telethon.tl.functions.users import GetFullUserRequest
from messages import collect_users_from_chat

logger = logging.getLogger(__name__)

async def get_user_details(client, user_id: int):
    try:
        user_entity = await client.get_entity(user_id)
        user_full = await client(GetFullUserRequest(user_id))

        name = f"{user_entity.first_name or ''} {user_entity.last_name or ''}".strip()
        username = user_entity.username or ""
        about = user_full.full_user.about or ""

        return {
            "name": name,
            "username": username,
            "about": about
        }
    except Exception as e:
        logger.error(f"Ошибка получения данных пользователя {user_id}: {e}")
        return None

async def parse_chat_users(client, chat_id_or_username: str, days: int = 30):
    try:
        # Проверяем, является ли chat_id_or_username числом (ID) или строкой (username)
        if chat_id_or_username.isdigit():
            chat = await client.get_entity(int(chat_id_or_username))
        else:
            chat = await client.get_entity(chat_id_or_username)

        user_stats = await collect_users_from_chat(client, chat, days)
        if not user_stats:
            logger.info("Нет данных для сохранения.")
            return []

        result = []
        for user_id, stats in user_stats.items():
            details = await get_user_details(client, user_id)
            if details:
                details["message_count"] = stats["count"]
                details["last_message_date"] = stats["last_message"].strftime("%Y-%m-%d %H:%M:%S")
                result.append(details)

        logger.info(f"Собрано данных: {len(result)} пользователей.")
        return result
    except Exception as e:
        logger.error(f"Ошибка при получении информации о чате {chat_id_or_username}: {e}")
        return []

