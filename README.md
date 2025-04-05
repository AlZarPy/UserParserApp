# Telegram User Parser

Простое приложение для сбора пользователей из чатов Telegram с возможностью экспорта в `.csv` файл.

## Возможности

- Авторизация по номеру телефона
- Загрузка и отображение доступных чатов (каналы и группы)
- Сбор пользователей из заданного чата за выбранное количество дней
- Экспорт данных в `user_data.csv`
- Конфигурация API сохраняется в `config.json`
- Поддержка сборки в `.exe` без вшивания конфигурации

## Установка

1. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

2. Запустите приложение:
   ```bash
   python main.py
   ```

## Сборка в `.exe`

Для создания исполняемого файла:

```bash
pyinstaller --onefile main.py
```

> ⚠️ Файл `config.json` НЕ вшивается в `.exe`, а создается в той же папке при первом запуске.

## Структура проекта

```
.
├── main.py               # Точка входа
├── create_config.py      # Создание/загрузка конфигурации
├── dialogs.py            # Получение списка каналов/групп
├── users.py              # Сбор пользователей
├── export.py             # Сохранение в CSV
├── config.json           # Конфиг с api_id, api_hash и телефоном (автосоздается)
├── requirements.txt
```

## Пример `config.json`

```json
{
  "api_id": 123456,
  "api_hash": "your_api_hash",
  "phone": "+1234567890"
}
```

## Требования

- Python 3.10+
- Библиотека Telethon

## Лицензия

MIT