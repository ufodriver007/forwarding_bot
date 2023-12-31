from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config


# Получаем данные из переменных окружения
config: Config = load_config('.env')

# Инициализируем бот и диспетчер
bot: Bot = Bot(token=config.tg_bot.token)
dp: Dispatcher = Dispatcher()
