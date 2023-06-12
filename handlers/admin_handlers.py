from aiogram import Router, Bot
from filters.custom_filters import IsAdmin, IsInfoText, ReplacementRule
from aiogram.types import Message, ChatInviteLink
from aiogram.filters import Command, CommandStart
from keyboards.chats_choosing import inl_add_keyboard
from keyboards.admins_chats_choosing import admins_chats_kb_builder
from keyboards.simple_row import make_simple_keyboard, skip_keyboard
from aiogram.filters import Text
from aiogram.types import ReplyKeyboardRemove
from filters.custom_filters import FromCorrectChat, CustomBaseFilter, FilterIn
from models.resend import send_to_admin
from models.db import db, cursor, select_all, get_from_channel_list, get_all_chats, add_new_forwarding, get_chat_name_from_id, delete_rule
from aiogram.fsm.context import FSMContext
from states.forwarding_states import SetConfig
from aiogram.types import CallbackQuery
from keyboards.chats_choosing import inl_del_keyboard
from create_bot import config


# Инициализируем роутер
router: Router = Router()
router.message.filter(IsAdmin(), FromCorrectChat())


# Меню конфигурации /start
@router.message(CommandStart())
async def conf_command(message: Message):
    await message.answer(text='Создать пересылку /forwarding \n'
                              'Удалить пересылку /delete_forwarding \n'
                              'Список пересылок /forwarding_list \n'
                              'Список чатов /chats')


@router.message(Command(commands='cancel'))
async def cancel_command(message: Message, state: FSMContext):
    await message.answer(text='Отменено')
    await state.clear()


# комманда /forwarding Создание перенаправления
@router.message(Command(commands='forwarding'))
async def forwarding_command(message: Message, state: FSMContext):
    await message.answer(text='Создание пересылки. Для начала выберите канал откуда нужно пересылать сообщения. Комманда /cancel для отмены')
    chats = get_all_chats()
    for chat in chats:
        await message.answer(text=f'{chat[0]} {chat[1]}', reply_markup=inl_add_keyboard)

    await state.set_state(SetConfig.cf_choosing_from_channel)


# продолдение диалога создания перенаправления
@router.callback_query(SetConfig.cf_choosing_from_channel)
async def forwarding_dialog(callback: CallbackQuery, state: FSMContext):
    await callback.answer()                                 # убирает часики.
    await state.update_data(from_channel=callback.message.text.split()[1])
    await callback.message.answer(text='Теперь нужно выбрать куда будут пересылаться сообщения. Комманда /cancel для отмены')
    await callback.message.delete()                         # Удаляем сообщение, в котором была нажата кнопка

    await callback.message.answer(text='В мой чат', reply_markup=inl_add_keyboard)
    chats = get_all_chats()
    for chat in chats:
        await callback.message.answer(text=f'{chat[0]} {chat[1]}', reply_markup=inl_add_keyboard)

    await state.set_state(SetConfig.cf_filter_in)


# продолжение диалога создания перенаправления
@router.callback_query(SetConfig.cf_filter_in)
async def forwarding_dialog(callback: CallbackQuery, state: FSMContext):
    await callback.answer()                                 # убирает часики.
    if callback.message.text.split()[1] == 'мой':
        admins = [int(x) for x in config.admin.telegram_id.split(',')]
        await state.update_data(to_channel=admins[0])
    else:
        await state.update_data(to_channel=callback.message.text.split()[1])
    await callback.message.answer(text='Что будем пересылать? Варианты фильтрации:\n'
                                       'contains <i>текст</i>\n'
                                       'not_contains <i>текст</i>\n'
                                       'starts <i>текст</i>\n'
                                       'ends <i>текст</i>\n'
                                       'Комманда /cancel для отмены', parse_mode='HTML')

    await callback.message.delete()                         # Удаляем сообщение, в котором была нажата кнопка
    await state.set_state(SetConfig.cf_filter_in)


# продолжение диалога создания перенаправления
@router.message(SetConfig.cf_filter_in, FilterIn())
async def forwarding_dialog(message: Message, state: FSMContext):
    await state.update_data(filter_in=message.text)
    await message.answer(text='Если нужно заменить слово/текст напишите <что заменить> <на что заменить>. Или же нажмите "Пропустить". Комманда /cancel для отмены', reply_markup=skip_keyboard)
    await state.set_state(SetConfig.cf_filter_out)


# неверно введены данные входного фильтра
@router.message(SetConfig.cf_filter_in)
async def forwarding_dialog(message: Message, state: FSMContext):
    await message.answer(text='Неверно введены данные. Варианты фильтрации:\n'
                              'contains <i>текст</i>\n'
                              'not_contains <i>текст</i>\n'
                              'starts <i>текст</i>\n'
                              'ends <i>текст</i>\n'
                              'Комманда /cancel для отмены', parse_mode='HTML')
    await state.set_state(SetConfig.cf_filter_in)


# конец дилога создания перенаправления
@router.message(SetConfig.cf_filter_out, ReplacementRule())
async def forwarding_dialog(message: Message, state: FSMContext):
    await state.update_data(filter_out=message.text)
    user_data = await state.get_data()
    await message.answer(text='Всё готово.', reply_markup=ReplyKeyboardRemove())
    if user_data["filter_out"] == 'Пропустить':
        user_data["filter_out"] = ''
    add_new_forwarding(user_data["from_channel"], user_data["to_channel"], user_data["filter_in"], user_data["filter_out"])
    await state.clear()


# неверно введены данные выходного фильтра
@router.message(SetConfig.cf_filter_out)
async def forwarding_dialog(message: Message):
    await message.answer(text='Нужно написать слово, которое нужно заменить, пробел, а затем ещё одно слово. Комманда /cancel для отмены')


# команда /delete_forwarding' удаление пересылки
@router.message(Command(commands='delete_forwarding'))
async def conf_command(message: Message, bot: Bot):
    await message.answer(text='Список пересылок:')
    forwarding_list = select_all()
    for rule in forwarding_list:
        await message.answer(text=f'{rule[4]} Из чата {get_chat_name_from_id(rule[0])} в чат {get_chat_name_from_id(rule[1])} по фильтру {rule[2]} с заменой {rule[3] if rule[3] else "(БЕЗ замены)"}', reply_markup=inl_del_keyboard)


# приём значения кнопки, какую именно пересылку нужно удалить
@router.callback_query(Text(startswith='button_delete_pressed'))
async def forwarding_dialog(callback: CallbackQuery):
    await callback.answer()                                 # убирает часики.
    await callback.message.answer(text='Пересылка удалена.')
    delete_rule(callback.message.text.split()[0])


# команда /forwarding_list список созданных перенаправлений
@router.message(Command(commands='forwarding_list'))
async def conf_command(message: Message, bot: Bot):
    await message.answer(text='Список пересылок:')
    forwarding_list = select_all()
    for rule in forwarding_list:
        await message.answer(text=f'Из чата {get_chat_name_from_id(rule[0])} в чат {get_chat_name_from_id(rule[1])} по фильтру {rule[2]} с заменой {rule[3] if rule[3] else "(БЕЗ замены)"}')


# список всех чатов, куда был добавлен бот
@router.message(Command(commands='chats'))
async def conf_command(message: Message):
    chats = get_all_chats()
    await message.answer(text='Список всех чатов, куда добавлен бот:')
    for chat in chats:
        await message.answer(text=chat[0])


# основной базовый фильтр
@router.message(CustomBaseFilter())
async def other_commands(message: Message, bot: Bot):
    channels: list[tuple] = select_all()
    target = ''
    filter_out = ''
    for channel in channels:
        if int(channel[0]) == message.chat.id:  # ('442689577', '43243244', 'contains astra', None, 2)
            target = channel[1]
            filter_out = channel[3]

    # если есть фильтр замены слов в сообщении, меняем текст
    text = message.text
    if filter_out:
        text = message.text.replace(filter_out.split()[0], filter_out.split()[1])

    # кому пересылаем
    if not target:
        await send_to_admin(f'От {message.from_user.first_name} {message.from_user.last_name if message.from_user.last_name is not None else ""}: {text}', bot)
    else:
        await bot.send_message(chat_id=int(target), text=text)

