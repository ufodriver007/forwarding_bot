"""
This is a resend module. It provides methods for distribution message to all admins.
"""
from aiogram import Router, Bot
from create_bot import config


admins = [int(x) for x in config.admin.telegram_id.split(',')]


async def send_to_admin(text: str, bot: Bot):
    for admin in admins:
        await bot.send_message(chat_id=admin, text=text)

