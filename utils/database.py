import sqlite3

class Database():
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_db()

    #Таблица пользователей
    def create_db(self):
        try:
            query = ("CREATE TABLE IF NOT EXISTS bot_users("
                     "id INTEGER PRIMARY KEY,"
                     "chat_id TEXT UNIQUE,"
                     "user_name TEXT UNIQUE);")

            messager = ("CREATE TABLE IF NOT EXISTS bot_mails("
                     "id INTEGER PRIMARY KEY,"
                     "mes_text TEXT UNIQUE);")

            self.cursor.execute(query)
            self.cursor.execute(messager)
            self.connection.commit()
        except sqlite3.Error as Error:
            print("Ошибка прои создании", Error)


    def add_user(self, chat_id, user_name):
        try:
            self.cursor.execute(
                "INSERT OR IGNORE INTO bot_users (chat_id, user_name) VALUES (?,?)",
                (chat_id, user_name)
            )
            self.connection.commit()
            # Проверка успешности операции вставки
            if self.cursor.rowcount > 0:
                print(f"Запись успешно добавлена в базу данных - add_usser {chat_id} + {user_name}")
                return True
            else:
                print(f"Не удалось добавить пользователя {chat_id} {user_name} в базу данных.")
                return False
        except Exception as error:
            print(f"Ошибка при добавлении записи: {error}")
            return False


    def add_or_update_sms(self, sms_id, sms_text):
            try:
                self.cursor.execute(
                    "INSERT OR REPLACE INTO bot_mails (id, mes_text) VALUES (?, ?)",
                    (sms_id ,sms_text)
                )
                self.connection.commit()
                # Проверка успешности операции вставки
                if self.cursor.rowcount > 0:
                    print(f"Запись успешно добавлена в базу данных - add_sms {sms_text}")
                    return True
                else:
                    print(f"Не удалось добавить sms {sms_text} в базу данных.")
                    return False
            except Exception as error:
                print(f"Ошибка при добавлении записи: {error}")
                return False



    def get_user(self):
        try:
            query = "SELECT * FROM bot_users"
            self.cursor.execute(query)
            users = self.cursor.fetchall()
            return [user for user in users]
        except sqlite3.Error as error:
            print(f"Ошибка при получении пользователей: {error}")
            return None


    def get_message(self):
        try:
            query = "SELECT * FROM bot_mails"
            self.cursor.execute(query)
            messages = self.cursor.fetchall()
            return [sms for sms in messages]
        except sqlite3.Error as error:
            print(f"Ошибка при получении пользователей: {error}")
            return None
