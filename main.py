import random
import aiogram

from aiogram.dispatcher.filters.state import StatesGroup,State
from aiogram import Bot, Dispatcher, executor, types,exceptions
from aiogram.dispatcher.filters import Text
from config import TOKEN_API
import Keyboard
from Keyboard import keyboard, ikb, inkk, kb, ikb2 , kb_medeu, ink_medeu, ink_medeu2, \
    ink_session_workingDays, Nextink
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from sqlite import *
from datetime import datetime


flag = Falsestorage = MemoryStorage()
bot = Bot(TOKEN_API)
dp = Dispatcher(bot, storage=MemoryStorage())
ADMIN_ID = 1015079692


HELP_COMMAND = """
/help - list of commands
/start - for starting Bot
/Medeu - some information about Medeu(With lifeHacks)
/Random - get some random photos
/log - log in
/dick - grow dick
/top_dick - top rang
/show_last_data_play - Last data
/show_current_data - Current data
"""
arr_photos = [
    "https://i.pinimg.com/564x/0c/6b/7b/0c6b7bfe44ec0d273ac086322feda6e5.jpg",
    "https://i.pinimg.com/564x/81/43/10/81431081318e973eb31c7e6c24276b17.jpg",
    "https://i.pinimg.com/564x/34/f3/07/34f307995dd40ce5370d37b9cd4ecc4f.jpg",
    "https://i.pinimg.com/564x/c4/51/af/c451af8fc8de69d2b5ce48eeff602522.jpg",
    ""
]

photos = dict(zip(arr_photos, ['1','2','3','4']))

arr_photos_lifehacks = [
    "https://i.pinimg.com/564x/23/75/43/2375438815779b591831965cb05e2676.jpg",
    "https://i.pinimg.com/564x/5f/02/8c/5f028c8da50ffa5f4e5d5ebf5ba9c63c.jpg",
    "https://i.pinimg.com/564x/72/ed/85/72ed857d648c0d4ced2e581bbc41c19f.jpg",
    "https://i.pinimg.com/236x/ae/73/cb/ae73cb7dc4b964784aa89d9e33717d33.jpg",
    "https://i.pinimg.com/236x/b4/7b/9e/b47b9e96654d62d5dd35ac1100db95c6.jpg"
]
lifehack_photos = dict(zip(arr_photos_lifehacks,["Приходи в хорошем настроении!✨",
                                                 "Завяжи коньки покрепче, чтобы он фиксировал голеностоп, верхние(последние 3-4) люверсы затяни туже чем предыдушие, но не переборщи😅",
                                                 f"Можно купить шнурки с пропиткой, они лучше держат шнуровку, но тяжело расшнуровать",
                                                 "Перед тем как завязывать лучше оборачивать шнурок трижды, так он будет лучше держать шнуровку",
                                                 "Надевайте чехол на коньки, если вы хотите куда либо сходить, например в уборную. Это вам сэкономит время, коньки не придется снимать,также вы продлите жизнь лезвию конька."]))
random_photo_lifehack = random.choice(list(lifehack_photos.keys()))

class ProfileStateGroup(StatesGroup):
    name = State()



async def on_startup(_):
    print('Bot was successfully started!')
    await db_start()
    print("Connected with DB")


async def send_random(message: types.Message):
    randomPhoto = random.choice(list(photos.keys()))
    await bot.send_photo(message.chat.id,
                         photo=randomPhoto,
                         caption=photos[randomPhoto],
                         reply_markup=ikb2)



@dp.message_handler(commands=['start'])
async def start_cm(message:types.Message):
    await message.answer('<em>Wellcome to our Telegram Bot!</em>',
                         parse_mode="HTML",
                         reply_markup=keyboard)
    await create_profile(user_id=message.from_user.id)
    await set_data_now(datetime.now().day)



@dp.message_handler(commands=['admin'])
async def admin(message: types.Message):
    user_id = await get_user_id(message.from_user.id)
    if user_id[0] == '1015079692':
        all = await get_all()
        await message.answer(all)
    else:
        "Ты не админ..."
@dp.message_handler(commands=['dick'])
async def load_new_count(message: types.Message) ->None:
    await set_last_data(datetime.now().day, message.from_user.id)

    chance = await chance_from_db(message.from_user.id)
    print(chance[0])

    if chance[0] == 0:
        rand = random.randint(-20,30)
        await new_count(rand, message.from_user.id)
        name = await name_from_db(message.from_user.id)
        count = await count_from_db(message.from_user.id)
        await message.answer(str(name[0]) + " твой писюн вырос на " + str(rand) + "см сейчас он равен: " + str(count[0]))
        await chance_set(message.from_user.id)
        await chance_set(message.chat.id)
    if chance[0] != 0:
        await message.answer("Ты уже играл! Следующая попытка завтра!")

    curdata = await get_last_data(message.from_user.id)
    nowdata = await get_now_date()
    if curdata != nowdata:
        await chance_set_zero(message.from_user.id)
    alluser = await get_all_user(message.from_user.id)
    await show_all_user(alluser, message)
@dp.message_handler(commands='show_last_data_play')
async def show_last_data(message: types.Message):
    last = await get_last_data(message.from_user.id)
    await message.answer("В последний раз ты играл " + str(last[0]) + " этого месяца")
@dp.message_handler(commands='show_current_data')
async def show_now_data(message: types.Message):
    now = await get_now_date()
    await message.answer("Сегодня " + str(now[0]) + " день этого месяца")
async def show_all(products:list, message:types.Message) -> None:
    for product in products:
        await message.answer(f"{product[2]}" + " ➾ " + f"<b>{product[3]}</b>" + "см\n" + "Занимает в топе " + f"{product[0]}" + " место!", parse_mode='HTML')

async def show_all_user(products:list, message:types.Message) -> None:
    for product in products:
        await message.answer(f"{product[2]}" + " ➾ " + f"<b>{product[3]}</b>" + "см\n" + "Ты занимаешь в топе " + f"{product[0]}" + " место!", parse_mode='HTML')


async def show_count(products: list, message: types.Message):
    for product in products:
        await bot.send_message(chat_id=message.chat.id,text=f"{product[2]}")

@dp.message_handler(commands=['top_dick'])
async def top_dick(message: types.Message):
    all = await get_all()
    await show_all(all, message)





@dp.message_handler(commands=['log'])
async def logging(message: types.Message, state: FSMContext) -> None:
    await message.answer("Пришли мне свой ник!")
    await ProfileStateGroup.name.set()

@dp.message_handler(state=ProfileStateGroup.name)
async def load_name(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['name'] = message.text
    await edit_profile(state, user_id=message.from_user.id)
    await message.reply("Completed!")
    await ProfileStateGroup.next()
    await state.finish()

@dp.message_handler(commands=['help'])
async def help(message:types.Message):
    await message.answer(HELP_COMMAND)

@dp.message_handler(commands=['Medeu'])
async def Medeu(message:types.Message):
    await message.answer(text="Medeu",reply_markup=kb_medeu)

@dp.message_handler(Text(equals="Info"))
async def infoMedeu(message: types.Message):
    await message.answer(text="Высокогорный каток медеу\n"
                              "2Gis ссылка: https://go.2gis.com/hx27s"
                              ,reply_markup=ink_medeu)
    await message.delete()
@dp.message_handler(Text(equals="LifeHacks"))
async def lifehack(message: types.Message):
    await bot.send_photo(message.chat.id,
                         photo=random_photo_lifehack,
                         caption=lifehack_photos[random_photo_lifehack],
                         reply_markup=Nextink)
    await message.delete()
@dp.message_handler(commands=['give'])
async def start_cm(message:types.Message):
    await bot.send_sticker(message.chat.id,sticker= "CAACAgIAAxkBAAEG4Xdjn0CkTaL-WadR0Nean4tMbmulIAACbQ8AAvX64EopOdJWyR2ApywE")
    await bot.send_message(message.chat.id,text="LOL",reply_markup=ikb)
    await message.delete()

@dp.message_handler(commands=['loc'])
async def location(message: types.Message):
    await bot.send_location(chat_id=message.from_user.id,longitude=33,latitude=23)

@dp.message_handler(commands=['picture'])
async def pic(message: types.Message):
    await bot.send_photo(message.chat.id,photo="https://i.pinimg.com/564x/e3/11/c5/e311c52b0f472ebe9883e6bad20ec504.jpg")
    await bot.send_message(message.chat.id,text="Do you like it?",reply_markup=inkk)

@dp.message_handler(Text(equals="random_photo"))
async def random_photo(message: types.Message):

    await message.answer(text="Please choose button 'Random' ",
                         reply_markup=kb)


@dp.message_handler(Text(equals="/Random"))
async def SendRandomPhoto(message: types.Message):
    await send_random(message)


@dp.message_handler(Text(equals="Menu"))
async def menu(message: types.Message):
    await message.answer(text="Wellcome to main Menu",
                         reply_markup=keyboard)
    await message.delete()

@dp.callback_query_handler()
async def callbackall(callback: types.CallbackQuery):
    global random_photo_lifehack
    if callback.data == "like":
        await callback.answer(text="You like it✨")
    if callback.data == "Like":
        await callback.answer(text="You like it✨")
    if callback.data == "Dislike":
        await callback.answer(text="You Dislike it ")
    if callback.data == "Next":
        await send_random(message=callback.message)
    if callback.data == "price":
        await callback.message.answer(text="Выберите в какие дни:",reply_markup=ink_medeu2)
    if callback.data == "working_days":
        await callback.answer("❤️")
        await callback.message.answer(text="Выберите сеасн:", reply_markup=ink_session_workingDays)
    if callback.data == "session1_workingDays":
        await callback.answer("🤍")
        await callback.message.answer(text="10:00 - 12:30:\n"
                                      "Взрослый билет(23+) - 1000тг\n"
                                      "Молодежный билет(14-22) - 600тг\n"
                                      "Детский билет(7-13) - 500тг")
    if callback.data == "session2_workingDays":
        await callback.answer("💛")
        await callback.message.answer(text="13:30 - 16:30:\n"
                                           "Взрослый билет(23+) - 2000тг\n"
                                            "Молодежный билет(14-22) - 1200тг\n"
                                            "Детский билет(7-13) - 500тг",parse_mode="HTML")
    if callback.data == "session3_workingDays":
        await callback.answer("🤍")
        await callback.message.answer(text="19:00 - 23:00:\n"
                                           "Взрослый билет(23+) - 2500тг\n"
                                            "Молодежный билет(14-22) - 1500тг\n"
                                            "Детский билет(7-13) - 500тг")
    if callback.data == "days off":
        await callback.answer("🖤")
        await callback.message.answer(text="Soon...")
    if callback.data == "NextLifeHack":
        random_photo_lifehack = random.choice(list(filter(lambda x: x != random_photo_lifehack,list(lifehack_photos.keys()))))
        await callback.message.edit_media(types.InputMedia(media=random_photo_lifehack,type='photo',caption=lifehack_photos[random_photo_lifehack]),reply_markup=Nextink)
@dp.message_handler()
async def send_emoji(message: types.Message):
    if message.text == "thx":
        await message.reply("💗")

if __name__ == "__main__" :
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

