from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove,InlineKeyboardButton,InlineKeyboardMarkup

keyboard = ReplyKeyboardMarkup(resize_keyboard=True,
							   one_time_keyboard=False) #скрывает клаву после нажатия
b_help = KeyboardButton('/help')
b_start = KeyboardButton('/Medeu')
b_location = KeyboardButton('/Random')
b_picture = KeyboardButton('/picture')
keyboard.add(b_help).insert(b_start).add(b_location).insert(b_picture)

inkk = InlineKeyboardMarkup(row_width=2)
ibb = InlineKeyboardButton(text="❤️", callback_data="like")
ibb2 = InlineKeyboardButton(text="🤮", callback_data="dislike")
inkk.add(ibb).insert(ibb2)

ikb = InlineKeyboardMarkup(row_width=2)
ib = InlineKeyboardButton(text="Button1",
						  url="https://ru.pinterest.com/")
ib2 = InlineKeyboardButton(text="Button2",
						  url="https://ru.pinterest.com/")
ib3 = InlineKeyboardButton(text="Button3",
						  url="https://ru.pinterest.com/")

ikb2 = InlineKeyboardMarkup(row_width=2)
ib_1 = InlineKeyboardButton(text="Like",
                           callback_data="like")
ib_2 = InlineKeyboardButton(text="Dislike",
                           callback_data="Dislike")
ib_3 = InlineKeyboardButton(text="Next Photo",
                           callback_data="Next")
ikb2.add(ib_1, ib_2).add(ib_3)
ikb.add(ib).insert(ib2).add(ib3)

kb_medeu = ReplyKeyboardMarkup(resize_keyboard=True)
bm1 = KeyboardButton("Info")
bm2 = KeyboardButton("LifeHacks")
bm3 = KeyboardButton("Menu")
kb_medeu.add(bm1, bm2).add(bm3)

ink_medeu = InlineKeyboardMarkup()
M_inkb1 = InlineKeyboardButton("Цены",callback_data="price")
ink_medeu.add(M_inkb1)

ink_medeu2 = InlineKeyboardMarkup(row_width=2)
M2_inkb1 = InlineKeyboardButton("Будние дни",callback_data="working_days")
M2_inkb2 = InlineKeyboardButton("Выходные",callback_data="days off")
ink_medeu2.add(M2_inkb1, M2_inkb2)

ink_session_workingDays = InlineKeyboardMarkup(row_width=2)
sb1 = InlineKeyboardButton(text="10:00 - 12:30",callback_data="session1_workingDays")
sb2 = InlineKeyboardButton(text="13:30 - 16:30",callback_data="session2_workingDays")
sb3 = InlineKeyboardButton(text="19:00 - 23:00",callback_data="session3_workingDays")
ink_session_workingDays.add(sb1,sb2).add(sb3)


kb = ReplyKeyboardMarkup(resize_keyboard=True)
bp1 = KeyboardButton("Random")
bp2 = KeyboardButton("Menu")
kb.add(bp1,bp2)

Nextink = InlineKeyboardMarkup()
B1 = InlineKeyboardButton(text="next",callback_data="NextLifeHack")
Nextink.add(B1)