import json

import aiogram
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor, types
from config import api_token
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from main import get_rent_news

API_TOKEN = api_token
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class Form(StatesGroup):
    rrr = State()


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message, state: FSMContext):
    current_user = message.from_user.id
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton("Посты в ВК", callback_data="vk_pars")
    markup.add(button1)
    await message.answer(f"Здравствуйте! Выберите функцию:", reply_markup=markup)


@dp.callback_query_handler(lambda query: query.data in {'vk_pars'})
async def callback_giveaway(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == 'vk_pars':
        get_rent_news()
        with open('data/data.json') as file:
            lst = json.load(file)
        for text in lst:
            await callback_query.message.answer(text)


if __name__ == '__main__':
    executor.start_polling(dp)
