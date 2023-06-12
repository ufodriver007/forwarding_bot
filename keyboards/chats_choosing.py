from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from models.db import get_all_chats, select_all


# chats = get_all_chats()
#
# # инициализируем билдер
# chats_kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
#
# # создаём список с кнопками
# buttons: list[InlineKeyboardButton] = [InlineKeyboardButton(text='Добавить', callback_data=f'{chat[1]}') for chat in chats]
#
# # добавляем в билдер кнопки
# chats_kb_builder.row(*buttons)


# Создаем объекты инлайн-кнопок
button_add: InlineKeyboardButton = InlineKeyboardButton(
    text='Добавить',
    callback_data='button_add_pressed')

# Создаем объект инлайн-клавиатуры
inl_add_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[button_add]])


# Создаем объекты инлайн-кнопок
button_delete: InlineKeyboardButton = InlineKeyboardButton(
    text='Удалить',
    callback_data='button_delete_pressed')

# Создаем объект инлайн-клавиатуры
inl_del_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[button_delete]])
