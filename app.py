from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import json
from config import api_token

from main import get_rent_news

API_TOKEN = api_token
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    current_user = message.from_user.username
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton("Получить данные", callback_data="vk_pars")
    markup.add(button1)
    await message.answer(
        f"Здравствуйте, {current_user}! Нажмите на кнопку и получите список квартир для аренды по городу Москва взятые из вк новостей от частных лиц:",
        reply_markup=markup)


@dp.callback_query_handler(lambda query: query.data == 'vk_pars')
async def callback_giveaway(callback_query: types.CallbackQuery):
    if callback_query.data == 'vk_pars':
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text="Идёт загрузка данных отсалось меньше минуты ..."
        )
        get_rent_news()
        with open('data/data.json') as file:
            lst = json.load(file)
        for text in lst:
            await callback_query.message.answer("Страница арендодателя: " + str(text[1]) + "\n" + text[0][:4000])
            await asyncio.sleep(1)


if __name__ == '__main__':
    executor.start_polling(dp)
