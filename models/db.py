import sqlite3
from create_bot import config


db = sqlite3.connect('sf_agent_db.sqlite')
cursor = db.cursor()

cursor.execute('''
               CREATE TABLE IF NOT EXISTS channels (
               id INTEGER PRIMARY KEY,
                from_channel TEXT NOT NULL,
                to_channel TEXT,
                filter_in TEXT,
                filter_out TEXT)''')

cursor.execute('''
               CREATE TABLE IF NOT EXISTS chats (
               id INTEGER PRIMARY KEY,
                chat TEXT NOT NULL,
                name TEXT)''')

# выполнить запросы(только для меняющих базу)
db.commit()


def select_all() -> list[tuple]:
    cursor.execute("SELECT from_channel, to_channel, filter_in, filter_out, id FROM channels")
    result = cursor.fetchall()
    channels: list[tuple] = []
    for res in result:
        channels.append(res)  # ('442689577', None, None, None)
    return channels


def delete_rule(rule_id: str):
    cursor.execute(f"DELETE FROM channels WHERE id={rule_id}")
    db.commit()


def get_from_channel_list() -> list[int]:
    """Все чаты из таблицы chats и администраторы"""
    rows = get_all_chats()
    chats = []
    admins = [int(x) for x in config.admin.telegram_id.split(',')]
    chats.extend(admins)
    for row in rows:
        chats.append(int(row[1]))

    return chats


def add_new_forwarding(from_channel, to_channel, filter_in, filter_out):
    cursor.execute(f"INSERT INTO channels (from_channel, to_channel, filter_in, filter_out) VALUES ('{from_channel}', '{to_channel}', '{filter_in}', '{filter_out}')")
    db.commit()


def add_new_channel(telegram_id: str, name: str):
    cursor.execute(f"INSERT INTO chats (chat, name) VALUES ('{telegram_id}', '{name}')")
    db.commit()


def delete_channel(telegram_id: str):
    cursor.execute(f"DELETE FROM chats WHERE chat={telegram_id}")
    db.commit()


def get_all_chats():
    cursor.execute("SELECT name, chat FROM chats")
    result = cursor.fetchall()
    chats: list[tuple] = []
    for res in result:
        chats.append(res)  # (2, 3125234313, DarkAstra)
    return chats


def get_chat_name_from_id(chat_id: str) -> str:
    cursor.execute("SELECT name, chat FROM chats")
    result = cursor.fetchall()
    for res in result:
        if res[1] == chat_id:
            return res[0]           # (2, 3125234313, DarkAstra)
    return 'Мой чат'
