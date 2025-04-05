from telethon.tl.types import Channel
from telethon.errors import SessionPasswordNeededError
import logging

logger = logging.getLogger(__name__)


async def get_all_channels(client):
    all_channels = []

    try:
        # Получаем все диалоги пользователя
        dialogs = await client.get_dialogs()

        for dialog in dialogs:
            # Проверяем, что это канал (супергруппа или канал)
            if isinstance(dialog.entity, Channel):
                channel_info = {
                    "name": dialog.entity.title,
                    "id": dialog.entity.id,
                    "username": dialog.entity.username,
                    "status": "Открытый" if dialog.entity.username else "Закрытый"
                }

                all_channels.append(channel_info)

        return all_channels
    except Exception as e:
        logger.error(f"Ошибка при получении каналов: {e}")
        return []
