from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Hello!"), KeyboardButton(text="Bye!")],
        [KeyboardButton(text="Secret")],
    ],
    resize_keyboard=True,
)
