# Demo Art Studio Telegram Bot

Демо-проект Telegram-бота для художественной студии. Без базы данных и внешних сервисов — только простой сценарий, чтобы показать, как будет выглядеть бот.

## Установка

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Настройка

Скопируйте `.env.example` в `.env` и заполните значения:

```bash
cp .env.example .env
```

## Запуск

```bash
python -m bot.main
```

## Где менять тексты и слоты

Все тексты и заготовки слотов лежат в `bot/texts.py` и `bot/keyboards.py`. Это демо, поэтому данные можно редактировать прямо в коде.
