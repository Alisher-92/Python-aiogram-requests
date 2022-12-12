from database import connect_database


class InitDB:
    def __init__(self):
        self.connection, self.cursor = connect_database("../database.sqlite")

    def __create_users_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name VARCHAR(150) NOT NULL,
            username VARCHAR(100) UNIQUE,
            chat_id INTEGER NOT NULL UNIQUE
        )""")

    def __create_cities_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS cities(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER REFERENCES users(id),
            city_name VARCHAR(15) NOT NULL,
            
            UNIQUE(user_id, city_name)
        )""")

    def start(self):
        self.__create_users_table()
        self.__create_cities_table()

        self.connection.commit()
        self.connection.close()


if __name__ == "__main__":
    InitDB().start()
