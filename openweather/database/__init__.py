import sqlite3


def connect_database(db_path: str = "database.sqlite"):
    connection_ = sqlite3.connect(db_path)
    cursor_ = connection_.cursor()
    return connection_, cursor_
