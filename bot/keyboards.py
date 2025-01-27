from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

btn_1 = InlineKeyboardButton(text='Проверить IMEI', callback_data='get')
btn_3 = InlineKeyboardButton(
    text='Купить', callback_data='buy'
)
btn_2 = InlineKeyboardButton(text='Test', callback_data='test')

keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[btn_1],]
)

keyboard_2 = InlineKeyboardMarkup(
    inline_keyboard=[[btn_2],]
)

keyboard_3 = InlineKeyboardMarkup(
    inline_keyboard=[[btn_3],]
)
