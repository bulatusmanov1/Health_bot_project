from datetime import datetime
from io import BytesIO
import matplotlib.pyplot as plt
import sqlite3

class BotDB:
    def __init__(self, db_file):
        """Инициализация соединения с бд"""
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        """Проверяем наличие пользователя в бд"""
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return bool(len(result.fetchall()))

    def get_user_id(self, user_id):
        """Достаем id юзера в бд по его user_id"""
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return result.fetchone()[0]
    
    def get_profile(self, user_id):
        """Достаём профиль пользователя"""
        user_id = self.get_user_id(user_id)
        result = self.cursor.execute("SELECT * FROM `users` WHERE `id` = ?", (user_id,))
        result = list(result.fetchone())
        if result[3]:
            result[3] = "М"
        else:
            result[3] = "Ж"
        return result

    def add_user(self, user_id):
        """Добавляем пользователя в бд"""
        self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))
        return self.conn.commit()

    def add_gender(self, user_id, gender):
        """Добавляем гендер пользователя в бд"""
        user_id = self.get_user_id(user_id)
        self.cursor.execute("UPDATE `users` SET `gender` = ? WHERE `id` = ?", (gender[0] == "М" or gender[0] == "м", user_id))
        return self.conn.commit()
    
    def add_age(self, user_id, age):
        """Добавляем возраст пользователя в бд"""
        user_id = self.get_user_id(user_id)
        self.cursor.execute("UPDATE `users` SET `age` = ? WHERE `id` = ?", (age, user_id))
        return self.conn.commit()
    
    def add_height(self, user_id, height):
        """Добавляем рост пользователя в бд"""
        user_id = self.get_user_id(user_id)
        self.cursor.execute("UPDATE `users` SET `height` = ? WHERE `id` = ?", (height, user_id))
        return self.conn.commit()
    
    def add_weight(self, user_id, weight):
        """Добавляем вес пользователя в бд"""
        user_id = self.get_user_id(user_id)
        self.cursor.execute("INSERT INTO `records` (`users_id`, `operations`, `value`) VALUES (?, ?, ?)",
            (user_id,
            1,
            weight))
        return self.conn.commit()
    
    def add_water(self, user_id, water):
        """Добавляем содержание воды пользователя в бд"""
        user_id = self.get_user_id(user_id)
        self.cursor.execute("INSERT INTO `records` (`users_id`, `operations`, `value`) VALUES (?, ?, ?)",
            (user_id,
            2,
            water))
        return self.conn.commit()
    
    def add_cal(self, user_id, cal):
        """Добавляем съеденные калории пользователя в бд"""
        user_id = self.get_user_id(user_id)
        self.cursor.execute("INSERT INTO `records` (`users_id`, `operations`, `value`) VALUES (?, ?, ?)",
            (user_id,
            3,
            cal))
        return self.conn.commit()
    
    def get_data(self, user_id, operations, within = "all", start_date = None, end_date = None):
        """Получаем данные из бд за опредилённый промежуток времени"""
        user_id = self.get_user_id(user_id)
        if start_date is None:
            if within == "day":
                result = self.cursor.execute("SELECT * FROM `records` WHERE `users_id` = ? AND `operations` = ? AND `date` BETWEEN datetime('now', 'start of day') AND datetime('now', 'localtime') ORDER BY `date`",
                    (user_id, operations))
            elif within == "week":
                result = self.cursor.execute("SELECT * FROM `records` WHERE `users_id` = ? AND `operations` = ? AND `date` BETWEEN datetime('now', '-6 days') AND datetime('now', 'localtime') ORDER BY `date`",
                    (user_id, operations))
            elif within == "month":
                result = self.cursor.execute("SELECT * FROM `records` WHERE `users_id` = ? AND `operations` = ? AND `date` BETWEEN datetime('now', 'start of month') AND datetime('now', 'localtime') ORDER BY `date`",
                    (user_id, operations))
            else:
                result = self.cursor.execute("SELECT * FROM `records` WHERE `users_id` = ? AND `operations` = ? ORDER BY `date`",
                    (user_id, operations))
            return result.fetchall()
        else:
            result = self.cursor.execute("SELECT * FROM `records` WHERE `users_id` = ? AND `date` BETWEEN ? AND ? AND `operations` = ? ORDER BY `date`", (user_id, start_date, end_date, operations))
            return result.fetchall()

    def draw_graf(self, user_id, operations, within = "all", value1 = 1, value2 = 1, start_date = None, end_date = None):
        """Строит график"""
        data = self.get_data(user_id, operations, within, start_date, end_date)

        if not data:
            return None

        values = [record[3] for record in data]
        dates = [datetime.strptime(record[4], "%Y-%m-%d %H:%M:%S") for record in data]

        plt.clf()
        plt.plot(dates, values, marker='o', linestyle='-', color='b')

        #Расчёты нормального состояния----------------------------------------------------------------------------
        if value1 == 1:
            parametrs = self.get_profile(user_id)
            if parametrs[3]:# если мужчина
                if operations == 1: # вес
                    if parametrs[4] <= 30 and parametrs[4] >= 20:
                        value1 = (parametrs[5] - 110) * 0.89
                    elif parametrs[4] >= 50:
                        value1 = (parametrs[5] - 110) * 1.06
                    else:
                        value1 = parametrs[5] - 110
                elif operations == 2: # вода
                    value1 = self.get_data(user_id, 1, "day")[-1][3] * 30
                else: # каллории
                    value1 = 10 * self.get_data(user_id, 1, "day",)[-1][3] + 6.25 * parametrs[5] - 5 * parametrs[4] + 5

            else:    
                if operations == 1:
                    if parametrs[4] <= 30 and parametrs[4] >= 20:
                        value1 = (parametrs[5] - 100) * 0.89
                    elif parametrs[4] >= 50:
                        value1 = (parametrs[5] - 100) * 1.06
                    else:
                        value1 = parametrs[5] - 100
                elif operations == 2:
                    value1 = (self.get_data(user_id, 1, "day",)[-1][3]) * 30
                else:
                    value1 = 10 * (self.get_data(user_id, 1, "day",)[-1][3]) + 6.25 * parametrs[5] - 5 * parametrs[4] - 161
        
        value1, value2 = value1 * 0.9, value1 * 1.1
        #---------------------------------------------------------------------------------------------------------
        plt.axhline(y=value1, color='g', linestyle='--')
        plt.axhline(y=value2, color='g', linestyle='--')
        plt.fill_between(dates, value1, value2, color='green')
        plt.xlabel('Дата и время')
        plt.ylabel('Значения')
        plt.grid(True)

        # Форматирование меток по оси x для лучшей читаемости
        plt.gca().xaxis_date('UTC')
        plt.gcf().autofmt_xdate()

        image_stream = BytesIO()
        plt.savefig(image_stream, format='png', bbox_inches='tight')
        plt.close()
        image_stream.seek(0)
        return image_stream
    
    def draw_diag(self, user_id, operations, within="all", total_value=100, start_date=None, end_date=None):
        """Рисует диаграмку воды, где 100% можно задавать самому"""
        data = self.get_data(user_id, operations, within, start_date, end_date)

        if total_value == 100:
            total_value = (self.get_profile(user_id)[5] - 100) * 30

        if not data:
            return None

        value = sum([record[3] for record in data])

        if (total_value - value) >= 0:            
            percentages = [value, total_value - value]
        else:
            percentages = [value]

        colors = ['blue'] + ['gray']
        plt.clf()
        plt.pie(percentages, labels=None, autopct='%1.1f%%', startangle=90, colors=colors)
        plt.axis('equal')

        image_stream = BytesIO()
        plt.savefig(image_stream, format='png', bbox_inches='tight')
        plt.close()
        image_stream.seek(0)

        return image_stream

    
    def close(self):
        """Закрываем соединение с бд"""
        self.connection.close()