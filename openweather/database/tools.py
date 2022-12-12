from database import connect_database


class BaseTools:
    """Базовый класс инструментов
    Нужен для подключения к БД"""

    def __init__(self):
        self.connection, self.cursor = connect_database()


class UserTools(BaseTools):
    """Набор инструментов по работе с таблицей Users"""

    def register_user(self, *, full_name: str, username: str, chat_id: int) -> None:
        # EAFP - Проще попросить прощения, чем разрешения
        try:
            self.cursor.execute("""INSERT INTO users (full_name, username, chat_id)
                VALUES (?, ?, ?)
            """, (full_name, username, chat_id))
        except:
            pass
        else:  # работает, если ошибка не произошла
            self.connection.commit()
        finally:
            self.connection.close()

    def get_user_id(self, chat_id: int) -> int:
        self.cursor.execute("""SELECT id 
            FROM users 
            WHERE chat_id = ?
        """, (chat_id,))
        user_id: int = self.cursor.fetchone()[0]  # (id, )
        self.connection.close()
        return user_id


class CityTools(BaseTools):
    """Набор инструментов по работе с таблицей Cities"""

    def save_city(self, user_id: int, city_name: str) -> bool:
        save_status = False
        try:
            self.cursor.execute("""INSERT INTO cities (user_id, city_name)
                VALUES (?, ?)
            """, (user_id, city_name))
        except:
            pass
        else:
            save_status = True
            self.connection.commit()
        finally:
            self.connection.close()
            return save_status

    def get_city_names(self, user_id: int) -> list:
        self.cursor.execute("""SELECT city_name
            FROM cities
            WHERE user_id = ?
        """, (user_id,))
        cities = [
            city[0].title()
            for city in self.cursor.fetchall()
        ]
        self.connection.close()
        return cities

    def remove_city(self, user_id: int, city_name: str) -> bool:
        self.cursor.execute("""DELETE FROM cities
            WHERE user_id = ? AND city_name = ?          
        """, (user_id, city_name))
        self.connection.commit()
        self.connection.close()
        return True
