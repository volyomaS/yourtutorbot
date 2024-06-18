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
    global is_chatting_enabled
    is_chatting_enabled = True
    await message.answer(f"Start chatting with you!")


@dp.message(Command(commands="end_chat"))
async def command_end_chat_handler(message: Message) -> None:
    global is_chatting_enabled
    is_chatting_enabled = False
    await message.answer(f"End chatting")


@dp.message()
async def echo_handler(message: Message) -> None:
    print("Get msg", message.text)
    global is_chatting_enabled
    if is_chatting_enabled:
        global llm, chat_history
        user_msg = message.text
        chat_history.append({"role": "user", "content": user_msg})
        llm_ans = llm.answer(chat_history)
        print(llm_ans)
        chat_history.append({"role": "assistant", "content": llm_ans})
        await message.answer(llm_ans)
    else:
        try:
            await message.send_copy(chat_id=message.chat.id)
        except TypeError:
            await message.answer("Undefined error")


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
    is_chatting_enabled = False
    chat_history = []
    asyncio.run(main())
