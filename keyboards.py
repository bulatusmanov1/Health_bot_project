from aiogram import types

#Начальное меню----------------------------------------------------------------------------------------
inline_btn_1 = types.InlineKeyboardButton('Профиль', callback_data='btn1')
inline_btn_2 = types.InlineKeyboardButton('Пополнить статистику', callback_data='btn2')
inline_btn_3 = types.InlineKeyboardButton('Визуализация', callback_data='btn3')
inline_btn_4 = types.InlineKeyboardButton('Редактировать', callback_data='btn4')
inline_btn_5 = types.InlineKeyboardButton('Краткая сводка', callback_data='btn5')

inline_kb_full_1 = types.InlineKeyboardMarkup().add(inline_btn_1)
inline_kb_full_1.add(inline_btn_2, inline_btn_3)
inline_kb_full_1.add(inline_btn_5, inline_btn_4)
#Пополнить статистику-----------------------------------------------------------------------------------
inline_btn_b = types.InlineKeyboardButton('Назад', callback_data='btnb')

inline_btn_6 = types.InlineKeyboardButton('Вес', callback_data='btn6') # 1
inline_btn_7 = types.InlineKeyboardButton('Вода', callback_data='btn7') # 2
inline_btn_8 = types.InlineKeyboardButton('Калории', callback_data='btn8') # 3

inline_kb_full_2 = types.InlineKeyboardMarkup().add(inline_btn_6, inline_btn_7, inline_btn_8)
inline_kb_full_2.add(inline_btn_b)
#Визуализация--------------------------------------------------------------------------------------------
inline_btn_9 = types.InlineKeyboardButton('Графики', callback_data='btn9')
inline_btn_10 = types.InlineKeyboardButton('Диаграмма воды', callback_data='btn10')

inline_kb_full_3 = types.InlineKeyboardMarkup().add(inline_btn_9, inline_btn_10)
inline_kb_full_3.add(inline_btn_b)
#Графики-------------------------------------------------------------------------------------------------
inline_btn_11 = types.InlineKeyboardButton('Вес', callback_data='btn11')
inline_btn_12 = types.InlineKeyboardButton('Вода', callback_data='btn12')
inline_btn_13 = types.InlineKeyboardButton('Калории', callback_data='btn13')

inline_kb_full_4 = types.InlineKeyboardMarkup().add(inline_btn_11, inline_btn_12, inline_btn_13)
inline_kb_full_4.add(inline_btn_b)
#Краткая сводка------------------------------------------------------------------------------------------
inline_btn_14 = types.InlineKeyboardButton("Подсчёт каллорий", url="https://rsport.ria.ru/20220514/kaloriynost-1788483172.html")

inline_kb_full_5 = types.InlineKeyboardMarkup().add(inline_btn_14)
inline_kb_full_5.add(inline_btn_b)
#Прочее--------------------------------------------------------------------------------------------------
inline_kb_full_b = types.InlineKeyboardMarkup().add(inline_btn_b)