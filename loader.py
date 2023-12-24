from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

token = '6833997482:AAGLF6SJjiF6yGBRVOTab08oFZUMAUonsCw'

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage = MemoryStorage())