from aiogram import executor
from loader import dp
from db import BotDB
import handlers

BotDB = BotDB('accaunt.db')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)