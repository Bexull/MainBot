import logging
import random
import os
import pymongo
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from datetime import datetime, timedelta
import openai
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import *

# настройки бота
API_TOKEN = TOKEN_API

# создаем объекты бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# подключаемся к базе данных MongoDB
client = pymongo.MongoClient(CLIENT)
db = client['telegram_bot']

#ChatGPT
openai.api_key = AI

# создаем коллекцию для хранения результатов пользователей
results = db['results']

# устанавливаем уровень логирования
logging.basicConfig(level=logging.INFO)

# обработчик команды /start
@dp.message_handler(commands=['start'])
async def handle_start_command(message: types.Message):
    await message.answer(message.from_user.username + '<em> Wellcome to our Telegram Bot!</em>',
                         parse_mode="HTML")


HELP_COMMAND = """
/help - list of commands
/start - for starting Bot
/dick - grow dick
/top - top in the group
"""
SCHEDULE_COMMAND = "/schedule - Schedule for group"


@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    chat_member = await bot.get_chat_member(chat_id, user_id)

    if (chat_id == -1001531484283 and chat_member.status == 'member') or user_id == 1015079692:
        await message.answer(HELP_COMMAND + SCHEDULE_COMMAND)
    else:
        await message.answer(HELP_COMMAND)

# обработчик команды /grow
last_used = {}
@dp.message_handler(commands=['grow'])
async def cmd_grow(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # находим пользователя в базе данных
    user = results.find_one({'chat_id': chat_id, 'user_id': user_id})

    # проверяем, прошел ли уже текущий день с момента последнего использования команды
    last_used = user.get('last_used') if user else None
    now_utc = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    if last_used and last_used >= now_utc:
        await message.answer('Ты уже играл! Следующая попытка завтра!')
        return

    # находим результат за предыдущий день
    result = results.find_one({'chat_id': chat_id, 'user_id': user_id, 'date': {
        '$gte': (now_utc - timedelta(days=1)), '$lt': now_utc}})

    if result:
        # если результат за предыдущий день уже есть, то добавляем новый результат к старому
        RandomValue = random.randint(-15,30)
        result_value = result['value'] + RandomValue
        results.update_one({'_id': result['_id']}, {'$set': {'value': result_value}})
        if RandomValue > 0:
            await message.answer(
                f'{message.from_user.username} твой писюн вырос на {RandomValue}см, сейчас он равен: {result_value}')
        if RandomValue < 0:
            await message.answer(
                f'{message.from_user.username} твой писюн сократился на {RandomValue}см, сейчас он равен: {result_value}')
    elif user:
        # если пользователь уже есть в базе данных, но результат за предыдущий день не найден, то создаем новую запись
        RandomValue = random.randint(-15, 30)
        result_value = RandomValue
        results.insert_one({'chat_id': chat_id, 'user_id': user_id, 'value': result_value, 'date': now_utc})
        if RandomValue > 0:
            await message.answer(f'{message.from_user.username} твой писюн вырос на {RandomValue}см, сейчас он равен: {result_value}')
        if RandomValue < 0:
            await message.answer(
                f'{message.from_user.username} твой писюн сократился на {RandomValue}см, сейчас он равен: {result_value}')
    else:
        # если пользователь не найден в базе данных, то создаем новую запись и сохраняем время первого использования команды
        RandomValue = random.randint(-15, 30)
        result_value = RandomValue
        results.insert_one({'chat_id': chat_id, 'user_id': user_id, 'value': result_value, 'date': now_utc, 'first_used': now_utc})
        if RandomValue > 0:
            await message.answer(
                f'{message.from_user.username} твой писюн вырос на {RandomValue}см, сейчас он равен: {result_value}')
        if RandomValue < 0:
            await message.answer(
                f'{message.from_user.username} твой писюн сократился на {RandomValue}см, сейчас он равен: {result_value}')

    # обновляем время последнего использования команды в UTC-формате
    results.update_one({'chat_id': chat_id, 'user_id': user_id}, {'$set': {'last_used': datetime.utcnow()}})

@dp.message_handler(commands=['ai'])
async def send(message: types.Message):
    text = message.text.replace("/ai",'')

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=text,
        temperature=0.9,
        max_tokens=2500,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop="exx"
    )
    await message.answer(response['choices'][0]['text'])


# обработчик команды /top
@dp.message_handler(commands=['top'])
async def cmd_top(message: types.Message):
    chat_id = message.chat.id

    # находим все результаты для пользователей этой группы
    group_results = results.find({'chat_id': chat_id}).sort('value', pymongo.DESCENDING)

    if (count := results.count_documents({'chat_id': chat_id})) == 0:
        await message.answer('Нет результатов для этой группы.')
    else:
        # формируем строку с результатами
        result_str = '<b>------Топ игроков------</b>\n\n'
        for i, result in enumerate(group_results):
            user = await bot.get_chat_member(chat_id, result['user_id'])
            result_str += f"{i+1}| {user.user.username} ➾ {result['value']}\n"

        await message.answer(result_str,parse_mode='HTML')

@dp.message_handler(commands=['top_10'])
async def cmd_top_global(message: types.Message):
    # находим все результаты из базы данных, сортируем по убыванию значения и берем первые 10
    top_results = results.find().sort('value', pymongo.DESCENDING).limit(10)

    # формируем строку с результатами
    result_str = '<b>----Глобальный TOP‒10----</b>\n\n'
    for i, result in enumerate(top_results):
        chat_name = (await bot.get_chat(result['chat_id'])).title
        user = await bot.get_chat_member(result['chat_id'], result['user_id'])
        result_str += f"{i+1}|  {user.user.username} ➾ {result['value']} см\n"

    await message.answer(result_str,parse_mode='HTML')

@dp.message_handler(commands=['schedule'])
async def Schedule(message: types.Message):
    if message.chat.id == -1001531484283 or message.from_user.id == 1015079692:
        # Создаем клавиатуру
        keyboard = InlineKeyboardMarkup(row_width=2)
        btn_rvt = InlineKeyboardButton("РВТ", callback_data="rvt")
        btn_rsr = InlineKeyboardButton("РСР", callback_data="rsr")
        btn_rpt = InlineKeyboardButton("РПТ", callback_data="rpt")
        btn_rsb = InlineKeyboardButton("РСБ", callback_data="rsb")
        keyboard.add(btn_rvt, btn_rsr, btn_rpt, btn_rsb)
        await message.answer("Выберите день недели:", reply_markup=keyboard)
    else:
        await message.answer("У вас нет доступа к этой команде.")
@dp.callback_query_handler(lambda c: c.data in ["rvt", "rsr", "rpt", "rsb"])
async def process_callback_button(callback_query: types.CallbackQuery):
    # Получаем текст кнопки
    button_text = callback_query.data

    # Отправляем соответствующий текст в ответ на callback_query
    if button_text == "rvt":
        await callback_query.message.answer("14:10 - 15:00 |	<i> _ENGLISH_ </i> | 205B\n14:10 - 15:00 |	<i> _ENGLISH_ </i> | 205B\n16:10 - 17:00 |	<i> _WEB_ </i> | 501M\n17:20 - 18:10 |	<i> _WEB_ </i> | 501M", parse_mode='HTML')
    elif button_text == "rsr":
        await callback_query.message.answer("13:10 - 14:00 | <i>  _WEB LC_ </i>| 801M\n14:10 - 15:00 | <i> _RUS_ </i> | 409B\n15:10 - 16:00 | <i> _RUS_ </i> | 409B", parse_mode='HTML')
    elif button_text == "rpt":
        await callback_query.message.answer("09:00 - 09:50 | <i> _ECT LC_ </i>| 906M \n10:00 - 10:50 | <i> _PC_ </i> | GYM \n11:00 - 11:50 | <i> _PC_ </i> | GYM", parse_mode='HTML')
    elif button_text == "rsb":
        await callback_query.message.answer(
            "10:00 - 10:50 | <i> _ECT PR_ </i> | 210M\n11:00 - 11:50 | <i> _ECT PR_ </i> | 210M\n12:10 - 13:00	<i>-------CHILL-------</i>\n13:10 - 14:00 | <i> _CISCO_ </i> | 706M\n14:10 - 15:00 | <i> _CISCO_ </i> | 706M\n15:10 - 16:00 | <i> _CISCO_ </i> | 706M",parse_mode='HTML')


        # запускаем бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
