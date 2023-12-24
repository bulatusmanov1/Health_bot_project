from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardRemove
from loader import dp
from app import BotDB
from states import CallbackOnStart
from aiogram import types
from keyboards import *
import re

#Первый запуск-------------------------------------------------------------------------------------------------

@dp.message_handler(commands = "start")
async def start(message: types.Message):
    if(not BotDB.user_exists(message.from_user.id)):
        BotDB.add_user(message.from_user.id)
        await message.bot.send_message(message.from_user.id, "Здравствуйте!")
        await message.answer('Укажите свой пол(М/Ж)')
        await CallbackOnStart.Q1.set()
    else:
        await message.bot.send_message(message.from_user.id, "Добро пожаловать!", reply_markup = inline_kb_full_1)

@dp.message_handler(state=CallbackOnStart.Q1)
async def gender(message: types.Message, state: FSMContext):
    BotDB.add_gender(message.from_user.id, message.text)
    await message.answer('Укажите свой возраст')
    await CallbackOnStart.Q2.set()

@dp.message_handler(state=CallbackOnStart.Q2)
async def age(message: types.Message, state: FSMContext):
    BotDB.add_age(message.from_user.id, message.text)
    await message.answer('Укажите свой рост')
    await CallbackOnStart.Q3.set()

@dp.message_handler(state=CallbackOnStart.Q3)
async def height(message: types.Message, state: FSMContext):
    BotDB.add_height(message.from_user.id, message.text)
    await message.answer("Спасибо за уделённое время", reply_markup = inline_kb_full_1)
    await state.finish()

#Выбор кнопки--------------------------------------------------------------------------------------------------------

@dp.callback_query_handler(lambda c: c.data == 'btnb') # Назад
async def back(callback_query: types.CallbackQuery):
    await dp.bot.send_message(callback_query.from_user.id, "Меню", reply_markup = inline_kb_full_1)

@dp.callback_query_handler(lambda c: c.data == 'btn1') # Профиль
async def profile(callback_query: types.CallbackQuery):
    result = '\n'.join(f"{num} {letter}" for num, letter in zip(["id в системе:", "id пользователя:", "дата подключения:", "пол:", "возраст:", "рост:"], BotDB.get_profile(callback_query.from_user.id)))
    await dp.bot.send_message(callback_query.from_user.id, result, reply_markup = inline_kb_full_b)

@dp.callback_query_handler(lambda c: c.data == 'btn2') # Пополнить статистику
async def stats(callback_query: types.CallbackQuery):
    await dp.bot.send_message(callback_query.from_user.id, "Статистика", reply_markup = inline_kb_full_2)

@dp.callback_query_handler(lambda c: c.data == 'btn3') # Визуализация
async def show(callback_query: types.CallbackQuery):
    await dp.bot.send_message(callback_query.from_user.id, "Визуализация", reply_markup = inline_kb_full_3)

@dp.callback_query_handler(lambda c: c.data == 'btn4') # Редактировать
async def change(callback_query: types.CallbackQuery):
    await dp.bot.send_message(callback_query.from_user.id, "Укажите свой пол(М/Ж)")
    await CallbackOnStart.Q1.set()

@dp.callback_query_handler(lambda c: c.data == 'btn5') # Краткая сводка
async def info(callback_query: types.CallbackQuery):
    await dp.bot.send_message(callback_query.from_user.id, "Бот помогает пользователю отслеживать свои параметры веса, контролировать уровень потребления воды, каллорийность и визуализировать эту информацию для лучшего понимания своего здоровья.", reply_markup = inline_kb_full_5)

@dp.callback_query_handler(lambda c: c.data == 'btn6') # Добавить вес
async def stats_weight(callback_query: types.CallbackQuery):
    await dp.bot.send_message(callback_query.from_user.id, "Введите свой вес")
    await CallbackOnStart.Q4.set()

@dp.callback_query_handler(lambda c: c.data == 'btn7') # Добавить воду
async def stats_water(callback_query: types.CallbackQuery):
    await dp.bot.send_message(callback_query.from_user.id, "Введите выпитое количество воды в мл")
    await CallbackOnStart.Q5.set()

@dp.callback_query_handler(lambda c: c.data == 'btn8') # Добавить калории
async def stats_cal(callback_query: types.CallbackQuery):
    await dp.bot.send_message(callback_query.from_user.id, "Введите cъеденное количество каллорий")
    await CallbackOnStart.Q6.set()

@dp.callback_query_handler(lambda c: c.data == 'btn9') # Графики
async def graf(callback_query: types.CallbackQuery):
    await dp.bot.send_message(callback_query.from_user.id, "Графики", reply_markup = inline_kb_full_4)

@dp.callback_query_handler(lambda c: c.data == 'btn10') # Диаграмма
async def diag(callback_query: types.CallbackQuery):
    try:
        image_stream = BotDB.draw_diag(callback_query.from_user.id, 2, "day")
        await dp.bot.send_photo(callback_query.from_user.id, image_stream, caption='Диаграмма воды', parse_mode = types.ParseMode.MARKDOWN, reply_markup = inline_kb_full_b)
    except:
        await dp.bot.send_message(callback_query.from_user.id, "Нет данных", reply_markup = inline_kb_full_b)


@dp.callback_query_handler(lambda c: c.data == 'btn11') # График веса
async def draw_weight(callback_query: types.CallbackQuery):
    try:
        await dp.bot.send_message(callback_query.from_user.id, "Введите за какое время вы хотите увидеть статистику(day/week/month/all)")
        await CallbackOnStart.Q7.set()
    except:
        await dp.bot.send_message(callback_query.from_user.id, "Нет данных", reply_markup = inline_kb_full_b)

@dp.callback_query_handler(lambda c: c.data == 'btn12') # График воды
async def draw_water(callback_query: types.CallbackQuery):
    try:
        await dp.bot.send_message(callback_query.from_user.id, "Введите за какое время вы хотите увидеть статистику(day/week/month/all)")
        await CallbackOnStart.Q8.set()
    except:
        await dp.bot.send_message(callback_query.from_user.id, "Нет данных", reply_markup = inline_kb_full_b)

@dp.callback_query_handler(lambda c: c.data == 'btn13') # График каллорий
async def draw_cal(callback_query: types.CallbackQuery):
    try:
        await dp.bot.send_message(callback_query.from_user.id, "Введите за какое время вы хотите увидеть статистику(day/week/month/all)")
        await CallbackOnStart.Q9.set()
    except:
        await dp.bot.send_message(callback_query.from_user.id, "Нет данных", reply_markup = inline_kb_full_b)

#Обработка кнопки-----------------------------------------------------------------------------------------------------
        
@dp.message_handler(state=CallbackOnStart.Q4)
async def process_weight(message: types.Message, state: FSMContext):
    BotDB.add_weight(message.from_user.id, message.text)
    await message.answer("Вес успешно сохранён", reply_markup = inline_kb_full_2)
    await state.finish()

@dp.message_handler(state=CallbackOnStart.Q5)
async def process_water(message: types.Message, state: FSMContext):
    BotDB.add_water(message.from_user.id, message.text)
    await message.answer("Выпитое количество воды успешно сохраненно", reply_markup = inline_kb_full_2)
    await state.finish()

@dp.message_handler(state=CallbackOnStart.Q6)
async def process_cal(message: types.Message, state: FSMContext):
    BotDB.add_cal(message.from_user.id, message.text)
    await message.answer("Cъеденное количество каллорий успешно сохраненно", reply_markup = inline_kb_full_2)
    await state.finish()

@dp.message_handler(state=CallbackOnStart.Q7)
async def process_draw_weight(message: types.Message, state: FSMContext):
    image_stream = BotDB.draw_graf(message.from_user.id, 1, message.text)
    await dp.bot.send_photo(message.from_user.id, image_stream, caption = 'График веса', parse_mode = types.ParseMode.MARKDOWN, reply_markup = inline_kb_full_3)
    await state.finish()

@dp.message_handler(state=CallbackOnStart.Q8)
async def process_draw_water(message: types.Message, state: FSMContext):
    image_stream = BotDB.draw_graf(message.from_user.id, 2, message.text)
    await dp.bot.send_photo(message.from_user.id, image_stream, caption = 'График воды', parse_mode = types.ParseMode.MARKDOWN, reply_markup = inline_kb_full_3)
    await state.finish()

@dp.message_handler(state=CallbackOnStart.Q9)
async def process_draw_cal(message: types.Message, state: FSMContext):
    image_stream = BotDB.draw_graf(message.from_user.id, 3, message.text)
    await dp.bot.send_photo(message.from_user.id, image_stream, caption='График калорий', parse_mode = types.ParseMode.MARKDOWN, reply_markup = inline_kb_full_3)
    await state.finish()





