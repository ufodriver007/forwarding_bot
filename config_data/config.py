from dataclasses import dataclass
from environs import Env


@dataclass
class Admin:
    telegram_id: str            # Токен для доступа к телеграм-боту


@dataclass
class TgBot:
    token: str            # Токен для доступа к телеграм-боту


@dataclass
class Config:
    tg_bot: TgBot
    admin: Admin


def load_config(path: str | None) -> Config:
    """Читаем переменные окружения ,записываем данные в экземпляр класса Config и возвращаем его"""
    env: Env = Env()
    env.read_env(path)

    return Config(tg_bot=TgBot(token=env('TOKEN')),
                  admin=Admin(telegram_id=env('ADMIN')))

# Anna id 229779340