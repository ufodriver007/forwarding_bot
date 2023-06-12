import asyncio
from aiogram import Bot
from create_bot import dp, bot
from aiogram.types import BotCommand
from handlers import admin_handlers, user_handlers, other_handlers


async def main() -> None:

    async def set_main_menu(bot: Bot):
        """Создаем список с командами и их описанием для кнопки menu"""
        main_menu_commands = [
            BotCommand(command='/start',
                       description='Начальная команда')]

        await bot.set_my_commands(main_menu_commands)

    async def on_startup():
        """автозагрузка"""
        await set_main_menu(bot)
        print('[INFO]Bot started')

    # Регистриуем роутеры в диспетчере
    dp.include_router(other_handlers.router_for_channels_transitions)
    dp.include_router(admin_handlers.router)
    dp.include_router(user_handlers.router)
    dp.startup.register(on_startup)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    asyncio.run(main())
