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
                        "messager_text TEXT,"
                        "messager_video TEXT UNIQUE);")

            messager_btns = ("CREATE TABLE IF NOT EXISTS messager_btns("
                    "id INTEGER PRIMARY KEY,"
                    "btn_id INTEGER,"
                    "btn_text TEXT,"
                    "btn_link,"
                    "FOREIGN KEY (btn_id) REFERENCES bot_mails(id));")

            channels = ("CREATE TABLE IF NOT EXISTS bot_channels("
                     "id INTEGER PRIMARY KEY,"
                     "channel_id TEXT UNIQUE," 
                     "channel_name TEXT UNIQUE,"
                     "channel_link TEXT UNIQUE);")

            greeting = ("CREATE TABLE IF NOT EXISTS bot_greeting("
                        "id INTEGER PRIMARY KEY,"
                        "greeting_id INTEGER UNIQUE,"
                        "greeting_text TEXT,"
                        "greeting_video TEXT UNIQUE,"
                        "FOREIGN KEY (greeting_id) REFERENCES bot_channels(id));")

            btns = ("CREATE TABLE IF NOT EXISTS greeting_btns("
                    "id INTEGER PRIMARY KEY,"
                    "btn_id INTEGER,"
                    "btn_text TEXT,"
                    "btn_link,"
                    "FOREIGN KEY (btn_id) REFERENCES bot_channels(id));")

            self.cursor.execute(query)
            self.cursor.execute(messager)
            self.cursor.execute(messager_btns)
            self.cursor.execute(channels)
            self.cursor.execute(greeting)
            self.cursor.execute(btns)
            self.connection.commit()
        except Exception as error:
            with open('databaseErrors.txt', 'a') as error_file:
                error_message = f"Ошибка при создании базы данных - {error}\n"
                error_file.write(error_message)
                print("Ошибка при создании базы данных", error)



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
                with open('databaseErrors.txt', 'a') as error_file:
                    error_message = f"Не удалось добавить пользователя {chat_id} {user_name} в базу данных.\n"
                    error_file.write(error_message)
                print(f"Не удалось добавить пользователя {chat_id} {user_name} в базу данных.")
                return False
        except Exception as error:
            with open('databaseErrors.txt', 'a') as error_file:
                error_message = f"Ошибка при попытке добавить пользователя в базу данных - {error}\n"
                error_file.write(error_message)
            print("Ошибка при попытке добавить пользователя в базу данных", error)
            return False





    def get_user(self):
        try:
            query = "SELECT * FROM bot_users"
            self.cursor.execute(query)
            users = self.cursor.fetchall()
            return [user for user in users]
        except sqlite3.Error as error:
            with open('databaseErrors.txt', 'a') as error_file:
                error_message = f"Ошибка при получении пользователей: {error}\n"
                error_file.write(error_message)
            print(f"Ошибка при получении пользователей: {error}")
            return None



    def add_channels(self,channel_id, channel_name, channel_link):
        try:
            self.cursor.execute(
                "INSERT OR IGNORE INTO bot_channels (channel_id, channel_name, channel_link) VALUES (?,?,?)",
                (channel_id, channel_name, channel_link)
            )
            self.connection.commit()
            # Проверка успешности операции вставки
            if self.cursor.rowcount > 0:
                print(f"Запись успешно добавлена в базу данных - add_channels {channel_id} + {channel_name} + {channel_link}")
                return True
            else:
                with open('databaseErrors.txt', 'a') as error_file:
                    error_message = f"Не удалось добавить канал {channel_id} + {channel_name} + {channel_link} в базу данных.\n"
                    error_file.write(error_message)
                print(f"Не удалось добавить канал {channel_id} + {channel_name} + {channel_link} в базу данных.")
                return False
        except Exception as error:
            with open('databaseErrors.txt', 'a') as error_file:
                error_message = f"Ошибка при попытке добавить канал в базу данных - {error}\n"
                error_file.write(error_message)
            print("Ошибка при попытке добавить канал в базу данных", error)
            return False



    def get_channels(self):
        try:
            query = "SELECT * FROM bot_channels"
            self.cursor.execute(query)
            channels = self.cursor.fetchall()
            return [channel for channel in channels]
        except sqlite3.Error as error:
            with open('databaseErrors.txt', 'a') as error_file:
                error_message = f"Ошибка при получении каналов: {error}\n"
                error_file.write(error_message)
            print(error_message)
            return None



    def add_or_update_greeting_video(self,channel_id, video_file):
        try:
            self.cursor.execute("SELECT greeting_id FROM bot_greeting WHERE greeting_id = ?", (channel_id,))
            record = self.cursor.fetchone()

            if record:
                self.cursor.execute("UPDATE bot_greeting SET greeting_video = ? WHERE greeting_id = ?", (video_file, channel_id))
            else:
                self.cursor.execute("INSERT INTO bot_greeting (greeting_id, greeting_video) VALUES (?, ?)",
                                    (channel_id, video_file))
            self.connection.commit()

            if self.cursor.rowcount > 0:
                print(f"Запись успешно добавлена в базу данных - add_or_update_greeting_video {channel_id} + {video_file}")
                return True
            else:
                with open('databaseErrors.txt', 'a') as error_file:
                    error_message = f"Запись успешно добавлена в базу данных - add_or_update_greeting_video {channel_id} + {video_file}\n"
                    error_file.write(error_message)
                print(error_message)
                return False
        except sqlite3.Error as error:
            with open('databaseErrors.txt', 'a') as error:
                error_message = f"Ошибка при добавлении/обновлении приветствия video: {error}\n"
                error_file.write(error_message)
            print(error_message)
            return False



    def add_or_update_greeting_text(self,channel_id, greeting_text):
        try:
            self.cursor.execute("SELECT greeting_id FROM bot_greeting WHERE greeting_id = ?", (channel_id,))
            record = self.cursor.fetchone()
            if record:
                self.cursor.execute("UPDATE bot_greeting SET greeting_text = ? WHERE greeting_id = ?",
                                    (greeting_text, channel_id))
            else:
                self.cursor.execute("INSERT INTO bot_greeting (greeting_id, greeting_text) VALUES (?, ?)",
                                    (channel_id, greeting_text))
            self.connection.commit()
            if self.cursor.rowcount > 0:
                print(f"Запись успешно добавлена в базу данных - add_or_update_greeting_text {channel_id} + {greeting_text}")
                return True
            else:
                with open('databaseErrors.txt', 'a') as error_file:
                    error_message = f"Запись успешно добавлена в базу данных - add_or_update_greeting_text {channel_id} + {greeting_text}\n"
                    error_file.write(error_message)
                print(error_message)
                return False
        except sqlite3.Error as e:
            with open('databaseErrors.txt', 'a') as error:
                error_message = f"Ошибка при добавлении/обновлении приветствия text: {error}\n"
                error_file.write(error_message)
            print(error_message)
            return False



    def add_or_update_greeting_btn(self,greeting_id, btn_text, btn_link):
        try:
            self.cursor.execute("INSERT OR REPLACE INTO greeting_btns (btn_id, btn_text, btn_link) VALUES (?,?,?)",
                                (greeting_id, btn_text, btn_link))
            self.connection.commit()
            if self.cursor.rowcount > 0:
                print(f"Запись успешно добавлена в базу данных - add_or_update_greeting_btn {greeting_id} + {btn_text} + {btn_link}")
                return True
            else:
                with open('databaseErrors.txt', 'a') as error_file:
                    error_message = f"Запись успешно добавлена в базу данных - add_or_update_greeting_btn {greeting_id} + {btn_text} + {btn_link}\n"
                    error_file.write(error_message)
                print(error_message)
                return False
        except sqlite3.Error as e:
            with open('databaseErrors.txt', 'a') as error:
                error_message = f"Ошибка при добавлении/обновлении приветствия btns: {error}\n"
                error_file.write(error_message)
            print(error_message)
            return False



    def select_channel_id(self, chat_id):
        try:
            self.cursor.execute("SELECT id FROM bot_channels WHERE channel_id = ?", (chat_id,))
            record_id = self.cursor.fetchone()
            if record_id is not None:
                return record_id[0]
            else:
                return None

        except Exception as error:

            with open('databaseErrors.txt', 'a') as error_file:
                error_message = f"Ошибка при попытке получить id записи с базу данных - {error}\n"
                error_file.write(error_message)
            print(error_message)

            return False

    def select_channel_info(self, channel_id):
        try:
            self.cursor.execute("SELECT greeting_text, greeting_video FROM bot_greeting WHERE greeting_id = ?", (channel_id,))
            greeting_data = self.cursor.fetchone()
            if greeting_data is not None:
                return greeting_data
            else:
                return None

        except Exception as error:

            with open('databaseErrors.txt', 'a') as error_file:
                error_message = f"Ошибка при попытке получить данные приветствия с базу данных - {error}\n"
                error_file.write(error_message)
            print(error_message)

            return False


    def select_channel_btns(self, channel_id):
        try:
            self.cursor.execute("SELECT btn_text, btn_link FROM greeting_btns WHERE btn_id = ?", (channel_id,))
            greeting_data = self.cursor.fetchone()
            if greeting_data is not None:
                return greeting_data
            else:
                return None

        except Exception as error:

            with open('databaseErrors.txt', 'a') as error_file:
                error_message = f"Ошибка при попытке получить данные кнопок с базу данных - {error}\n"
                error_file.write(error_message)
            print(error_message)

            return False



    def add_or_update_messenger_text(self,channel_id, messager_text):
        try:
            self.cursor.execute("SELECT id FROM bot_mails WHERE id = ?", (channel_id,))
            record = self.cursor.fetchone()
            if record:
                self.cursor.execute("UPDATE bot_mails SET messager_text = ? WHERE id = ?",
                                    (messager_text, channel_id))
            else:
                self.cursor.execute("INSERT INTO bot_mails (id, messager_text) VALUES (?, ?)",
                                    (channel_id, messager_text,))
            self.connection.commit()
            if self.cursor.rowcount > 0:
                print(f"Запись успешно добавлена в базу данных - add_or_update_messenger_text {channel_id} + {messager_text}")
                return True
            else:
                with open('databaseErrors.txt', 'a') as error_file:
                    error_message = f"Запись успешно добавлена в базу данных - add_or_update_messenger_text {channel_id} + {messager_text}\n"
                    error_file.write(error_message)
                print(error_message)
                return False
        except sqlite3.Error as e:
            with open('databaseErrors.txt', 'a') as error:
                error_message = f"Ошибка при добавлении/обновлении приветствия text: {error}\n"
                error_file.write(error_message)
            print(error_message)
            return False



    def add_or_update_messenger_video(self,channel_id, video_file):
        try:
            self.cursor.execute("SELECT id FROM bot_mails WHERE id = ?", (channel_id,))
            record = self.cursor.fetchone()

            if record:
                self.cursor.execute("UPDATE bot_mails SET messager_video = ? WHERE id = ?", (video_file, channel_id))
            else:
                self.cursor.execute("INSERT INTO bot_mails (id, messager_video) VALUES (?, ?)",
                                    (channel_id, video_file))
            self.connection.commit()

            if self.cursor.rowcount > 0:
                print(f"Запись успешно добавлена в базу данных - add_or_update_messenger_video {channel_id} + {video_file}")
                return True
            else:
                with open('databaseErrors.txt', 'a') as error_file:
                    error_message = f"Запись успешно добавлена в базу данных - add_or_update_messenger_video {channel_id} + {video_file}\n"
                    error_file.write(error_message)
                print(error_message)
                return False
        except sqlite3.Error as error:
            with open('databaseErrors.txt', 'a') as error:
                error_message = f"Ошибка при добавлении/обновлении приветствия video: {error}\n"
                error_file.write(error_message)
            print(error_message)
            return False


    def add_or_update_messenger_btn(self,btn_id, btn_text, btn_link):
        try:
            self.cursor.execute("INSERT OR REPLACE INTO messager_btns (btn_id, btn_text, btn_link) VALUES (?,?,?)",
                                (btn_id, btn_text, btn_link))
            self.connection.commit()
            if self.cursor.rowcount > 0:
                print(f"Запись успешно добавлена в базу данных - add_or_update_messenger_btn {btn_id} + {btn_text} + {btn_link}")
                return True
            else:
                with open('databaseErrors.txt', 'a') as error_file:
                    error_message = f"Запись успешно добавлена в базу данных - add_or_update_messenger_btn {btn_id} + {btn_text} + {btn_link}\n"
                    error_file.write(error_message)
                print(error_message)
                return False
        except sqlite3.Error as e:
            with open('databaseErrors.txt', 'a') as error:
                error_message = f"Ошибка при добавлении/обновлении приветствия btns: {error}\n"
                error_file.write(error_message)
            print(error_message)
            return False


    def select_messanger_info(self, channel_id):
        try:
            self.cursor.execute("SELECT messager_text, messager_video FROM bot_mails WHERE id = ?", (channel_id,))
            greeting_data = self.cursor.fetchone()
            if greeting_data is not None:
                return greeting_data
            else:
                return False

        except Exception as error:

            with open('databaseErrors.txt', 'a') as error_file:
                error_message = f"Ошибка при попытке получить данные приветствия с базу данных - {error}\n"
                error_file.write(error_message)
            print(error_message)

            return False


    def select_messanger_btns(self, channel_id):
        try:
            self.cursor.execute("SELECT btn_text, btn_link FROM messager_btns WHERE btn_id = ?", (channel_id,))
            greeting_data = self.cursor.fetchone()
            if greeting_data is not None:
                return greeting_data
            else:
                return False

        except Exception as error:

            with open('databaseErrors.txt', 'a') as error_file:
                error_message = f"Ошибка при попытке получить данные кнопок с базу данных - {error}\n"
                error_file.write(error_message)
            print(error_message)

            return False

    def delete_channel_data(self, channel_id):
        try:
            # Удаляем записи из связанной таблицы
            self.cursor.execute("DELETE FROM bot_greeting WHERE greeting_id = ?", (channel_id,))

            # Удаляем записи из связанной таблицы
            self.cursor.execute("DELETE FROM greeting_btns WHERE btn_id = ?", (channel_id,))

            # Затем удаляем запись из основной таблицы
            self.cursor.execute("DELETE FROM bot_channels WHERE id = ?", (channel_id,))

            # Фиксируем изменения
            self.connection.commit()

            return True

        except Exception as error:
            with open('databaseErrors.txt', 'a') as error_file:
                error_message = f"Ошибка при попытке удалить канал {channel_id} - {error}\n"
                error_file.write(error_message)
            print(error_message)
            return False



    def delete_messanger_data(self, messanger_id):
        try:
            self.cursor.execute("DELETE FROM messager_btns WHERE btn_id = ?", (messanger_id,))
            self.cursor.execute("DELETE FROM bot_mails WHERE id = ?", (messanger_id,))
            self.connection.commit()
            return True

        except Exception as error:

            with open('databaseErrors.txt', 'a') as error_file:
                error_message = f"Ошибка при попытке удалить данные рассылки {messanger_id} - {error}\n"
                error_file.write(error_message)
            print(error_message)

            return False



    def delete_bot_greeting(self, greeting_id):
        try:
            self.cursor.execute("DELETE FROM greeting_btns WHERE btn_id = ?", (greeting_id,))
            self.cursor.execute("DELETE FROM bot_greeting WHERE greeting_id = ?", (greeting_id,))
            self.connection.commit()
            return True

        except Exception as error:

            with open('databaseErrors.txt', 'a') as error_file:
                error_message = f"Ошибка при попытке удалить приветствие {greeting_id} - {error}\n"
                error_file.write(error_message)
            print(error_message)

            return False

