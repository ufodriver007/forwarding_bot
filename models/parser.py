from aiogram.types import Message
from models.db import db, cursor, select_all, get_from_channel_list


async def filter_parser(message: Message) -> bool:
    """Базовый фильтр"""
    channels: list[tuple] = select_all()
    # алгоритм сопоставляет правила фильтрации для каждого чата и возвращает результат
    rule = ''

    for channel in channels:
        print(channel)
        if int(channel[0]) == message.chat.id:  # ('442689577', None, None, None)
            rule = channel[2]

    if not rule:
        return False
    elif rule.startswith('contains'):
        return rule[9:] in message.text
    elif rule.startswith('not_contains'):
        return not (rule[13:] in message.text)
    elif rule.startswith('starts'):
        return message.text.startswith(rule[7:])
    elif rule.startswith('ends'):
        return message.text.endswith(rule[5:])
    return False
