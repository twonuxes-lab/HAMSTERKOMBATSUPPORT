import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

# --- НАСТРОЙКИ ---
BOT_TOKEN = "9217797856:AAG5kLHR_dePQ6lxhkuPS4yPeJbZLMT1vYk"
ADMIN_ID = 8820172508

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Переменная для хранения ID последнего юзера, который написал боту
last_user_id = None

# --- ХЕНДЛЕР ДЛЯ КОМАНДЫ /start ---
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Это служба поддержки Hamster Kombat 2.0.\n"
        "Напиши свой вопрос, и я передам его администратору."
    )

# --- ХЕНДЛЕР ДЛЯ ВСЕХ СООБЩЕНИЙ ---
@dp.message()
async def handle_messages(message: Message):
    global last_user_id

    # Если пишет админ (ты)
    if message.from_user.id == ADMIN_ID:
        if last_user_id:
            # Отправляем текст юзеру
            await bot.send_message(
                chat_id=last_user_id, 
                text=f"👨‍💻 **Администратор ответил:**\n\n{message.text}"
            )
            await message.answer("✅ Ответ отправлен пользователю.")
            # Очищаем ID, чтобы не отправить случайно дважды
            last_user_id = None 
        else:
            await message.answer("❌ Пока никто не писал боту, некому отвечать.")
    else:
        # Если пишет юзер
        last_user_id = message.from_user.id
        user_name = message.from_user.username or message.from_user.first_name
        
        admin_text = (
            f"📩 Новое сообщение от @{user_name}\n"
            f"ID: {last_user_id}\n"
            f"Текст: {message.text}"
        )
        
        # Отправляем тебе
        await bot.send_message(chat_id=ADMIN_ID, text=admin_text)
        # Отвечаем юзеру
        await message.answer("✅ Твое сообщение отправлено администратору. Ожидай ответа.")

# --- ЗАПУСК ---
async def main():
    print("Бот поддержки запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())