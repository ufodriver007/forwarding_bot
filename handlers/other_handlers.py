from aiogram.types import ChatMemberUpdated
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, MEMBER, KICKED, JOIN_TRANSITION, LEAVE_TRANSITION
from aiogram import Router, F, Bot
from models import db


# Инициализируем роутер
router_for_channels_transitions: Router = Router()
router_for_channels_transitions.my_chat_member.filter(F.chat.type.in_({"group", "supergroup", "channel"}))


@router_for_channels_transitions.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION))
async def bot_added_in_chat(event: ChatMemberUpdated, bot: Bot):
    print(f'[INFO]Добавлен в группу {event.chat.title}. Её ID {event.chat.id}')
    telegram_id = str(event.chat.id)
    name = event.chat.title
    # добавляем в БД
    db.add_new_channel(telegram_id, name)


@router_for_channels_transitions.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=LEAVE_TRANSITION))
async def bot_kicked_from_chat(event: ChatMemberUpdated, bot: Bot):
    telegram_id = str(event.chat.id)
    print(f'[INFO]Удалён из группы {event.chat.title}.')
    # удаляем из БД
    db.delete_channel(telegram_id)
