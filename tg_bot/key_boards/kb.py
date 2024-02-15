from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_story(id):
    kb = InlineKeyboardMarkup(
        inline_keyboard = [
        [InlineKeyboardButton(text='окуу', callback_data=f"read_{id}")]
    ])
    return kb

def set_of_stories(stories : list):
    kb = InlineKeyboardMarkup(
        inline_keyboard = [
    ])
    for i in stories[10]:
        kb.inline_keyboard.append([InlineKeyboardButton(text=i[1], callback_data=f"read_{i[0]}")])
    return kb

def get_stories():
    kb = InlineKeyboardMarkup(
        inline_keyboard = [
        [InlineKeyboardButton(text='Басыныз', callback_data=f"get_books")]
    ])
    return kb