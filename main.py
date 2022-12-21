import random
import aiogram

from aiogram import Bot, Dispatcher, executor, types,exceptions
from aiogram.dispatcher.filters import Text
from config import TOKEN_API
import Keyboard
from Keyboard import keyboard, ikb, inkk, kb, ikb2 , kb_medeu, ink_medeu, ink_medeu2, \
	ink_session_workingDays, Nextink

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)

HELP_COMMAND = """
/help - list of commands
/start - for starting Bot
/Medeu - some information about Medeu(With lifeHacks)
Random - get some random photos
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
async def on_startup(_):
	print('Bot was successfully started!')

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


@dp.message_handler(Text(equals="Random"))
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
		await callback.message.answer(text="Soon...")
	if callback.data == "session2_workingDays":
		await callback.answer("💛")
		await callback.message.answer(text="10:00 - 12:30:\n"
										   "Взрослый билет(23+) - 2000тг\n"
											"Молодежный билет(14-22) - 1200тг\n"
											"Детский билет(7-13) - 500тг",parse_mode="HTML")
	if callback.data == "session3_workingDays":
		await callback.answer("🤍")
		await callback.message.answer(text="13:30 - 16:30:\n"
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


