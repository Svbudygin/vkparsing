from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
import json


from config import api_token

from main import get_rent_news, get_rent_news1

API_TOKEN = api_token
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

class Form(StatesGroup):
    request_state = State()
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    current_user = message.from_user.username
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton("Получить данные", callback_data="vk_pars")
    button2 = InlineKeyboardButton("Ввести запрос самому", callback_data="vk_pars_sam")
    markup.add(button1, button2)
    await message.answer(
        f"Здравствуйте, {current_user}! Нажмите на кнопку и получите список квартир для аренды по городу Москва взятые из вк новостей от частных лиц или введите запрос самостоятельно:\nP.S. Мы советуем вводить запрос самостоятельно",
        reply_markup=markup)


@dp.callback_query_handler(lambda query: query.data in {'vk_pars', 'vk_pars_sam'})
async def callback_giveaway(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == 'vk_pars':
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text="Идёт загрузка данных оcталось меньше минуты ..."
        )
        get_rent_news()
        with open('data/data.json') as file:
            lst = json.load(file)
        for text in lst:
            await callback_query.message.answer("Страница арендодателя: " + str(text[1]) + "\n" + text[0][:4000])
            await asyncio.sleep(1)
    if callback_query.data == 'vk_pars_sam':
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text="Введите ваш запрос (Например,\"Аренда квартиры Москва\"):"
        )
        await Form.request_state.set()

@dp.message_handler(state=Form.request_state)
async def process_name(message: types.Message, state: FSMContext):
    await message.answer("Идёт загрузка данных оcталось меньше минуты ..."
    )
    get_rent_news1(message.text)
    with open(f'data/data{message.text}.json') as file:
        lst = json.load(file)
    for text in lst:
        await message.answer("Страница арендодателя: " + str(text[1]) + "\n" + text[0][:4000])
        await asyncio.sleep(1)
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp)
