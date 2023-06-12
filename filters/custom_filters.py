from aiogram.filters import BaseFilter
from aiogram.types import Message
from create_bot import config
from models.parser import filter_parser
from models.db import db, cursor, select_all, get_from_channel_list
import re


class IsAdmin(BaseFilter):
    """Является ли пишущий администратором"""
    async def __call__(self, message: Message) -> bool:
        admins = [int(x) for x in config.admin.telegram_id.split(',')]
        return message.from_user.id in admins


class IsInfoText(BaseFilter):
    """Проверка на специальный текст"""
    special_text = 'asdf'

    async def __call__(self, message: Message) -> bool:
        return bool(re.search(self.special_text, message.text, flags=re.IGNORECASE))


class FromCorrectChat(BaseFilter):
    """Проверка что сообщение только из отслеживаемых чатов + админы"""
    async def __call__(self, message: Message) -> bool:
        return message.chat.id in get_from_channel_list()


class CustomBaseFilter(BaseFilter):
    """Базовая фильтрующая функция"""
    async def __call__(self, message: Message) -> bool:
        return await filter_parser(message)


class ReplacementRule(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.text == 'Пропустить':
            return True
        return bool(re.fullmatch(r'^[^ ]+ [^ ]+$', message.text))


class FilterIn(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if len(message.text.split()) == 2:
            if message.text.split()[0] in ['contains', 'not_contains', 'starts', 'ends']:
                return True
        return False
