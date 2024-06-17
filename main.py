import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from huggingface_hub import login as hf_login

from keyboards.main_menu import set_main_menu
from llm import LLM

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


@dp.message(Command(commands="start_chat"))
async def command_start_chat_handler(message: Message) -> None:
    await message.answer(f"start chat button")


@dp.message()
async def echo_handler(message: Message) -> None:
    print("get msg", message.text)
    global llm
    await message.answer(llm.answer(message.text))


# @dp.message()
# async def echo_handler(message: Message) -> None:
#     try:
#         await message.send_copy(chat_id=message.chat.id)
#     except TypeError:
#         await message.answer("Nice try!")


async def main() -> None:
    with open("bot_token.pass", "r") as fin:
        tg_access_token = fin.readline()
    bot = Bot(
        token=tg_access_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    await set_main_menu(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    with open("huggingface_token.pass", "r") as fin:
        hf_access_token = fin.readline()
    hf_login(token=hf_access_token)
    llm = LLM()
    asyncio.run(main())
