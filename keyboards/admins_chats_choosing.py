from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from create_bot import config


admins = [int(x) for x in config.admin.telegram_id.split(',')]

# инициализируем билдер
admins_chats_kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

# создаём список с кнопками
buttons: list[InlineKeyboardButton] = [InlineKeyboardButton(text='Добавить', callback_data=f'{admin}') for admin in admins]

# добавляем в билдер кнопки
admins_chats_kb_builder.row(*buttons)
