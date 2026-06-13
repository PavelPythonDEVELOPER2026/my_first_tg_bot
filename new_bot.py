import asyncio
import os
from pathlib import Path
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder  # <- Добавили инструмент для кнопок
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")
TOKEN = os.getenv("TG_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Изменяем реакцию на команду /start
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    # 1. Создаем "конструктор" для наших кнопок
    builder = ReplyKeyboardBuilder()
    
    # 2. Добавляем сами кнопки с текстом
    builder.add(types.KeyboardButton(text="🐱 Хочу котика!"))
    builder.add(types.KeyboardButton(text="⛅ Погода"))
    
    # 3. Говорим кнопкам встать друг под другом (1 кнопка в ряду)
    builder.adjust(1)
    
    # 4. Отправляем сообщение вместе с кнопками
    await message.answer(
        f"Привет, {message.from_user.first_name}! Выбери кнопку:",
        reply_markup=builder.as_markup(resize_keyboard=True) # resize_keyboard делает их аккуратными
    )

# Обрабатываем нажатия на эти кнопки
@dp.message()
async def handle_buttons(message: types.Message):
    if message.text == "🐱 Хочу котика!":
        await message.answer("Здесь скоро будет случайный котик! На следующем шаге мы его запрограммируем.")
    elif message.text == "⛅ Погода":
        await message.answer("Здесь будет реальная погода. Настроим её чуть позже!")
    else:
        await message.answer(f"Ты написал: {message.text}")

async def main():
    print("=== БОТ С КНОПКАМИ ЗАПУСТИЛСЯ! ===")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())