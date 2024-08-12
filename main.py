import my_token_unsecure
import my_user_id
import asyncio
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.types import Message
import os
import logging
from datetime import datetime
import subprocess

# ========= INIT ============ #

script_dir = os.path.dirname(os.path.realpath(__file__))
filename = script_dir + str("/logs/") + \
    datetime.now().strftime("%d_%b_%Y_%A_logs.txt")

logging.basicConfig(format='---> (%(asctime)s, %(name)s, %(levelname)s): %(message)s', level=logging.INFO, handlers=[
    logging.FileHandler(filename=filename, mode="a"),
    logging.StreamHandler()
])
logging.basicConfig(level=logging.INFO)

bot = Bot(token=my_token_unsecure.Token)
dp = Dispatcher()
router = Router()

#############################


async def get_ip() -> str:
    """
    crutch fix later: made more stable, like use multiple sources if one fails
    if all fails send some message to the tg user
    """
    my_ip_2 = subprocess.run("curl ipinfo.io/ip", shell=True,
                             capture_output=True).stdout.decode("utf-8").strip()

    return my_ip_2


@router.message(Command("ip"))
async def ip_cmd(message: Message):
    ip = await get_ip()
    await message.answer(ip)


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

loop = asyncio.get_event_loop()
main_task = loop.create_task(main())
loop.run_until_complete(main_task)

pending = asyncio.all_tasks(loop=loop)

for task in pending:
    task.cancel()

group = asyncio.gather(*pending, return_exceptions=True)
loop.run_until_complete(group)
loop.close()
