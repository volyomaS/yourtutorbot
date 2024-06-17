from aiogram import Bot
from aiogram.types import BotCommand

__MAIN_MENU_COMMANDS: dict[str, str] = {
    '/start_chat': 'Start practicing English with Bot',
    '/end_chat': 'End practicing English with Bot',
}


async def set_main_menu(bot: Bot) -> None:
    main_menu_commands = [
        BotCommand(
            command=command,
            description=description
        ) for command, description in __MAIN_MENU_COMMANDS.items()
    ]
    await bot.set_my_commands(main_menu_commands)
