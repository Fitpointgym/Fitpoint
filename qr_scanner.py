import os
import sqlite3
import datetime
from config import DATABASE_PATH  # Импортируем путь из config

# Абсолютный путь к базе данных
db_path = DATABASE_PATH

# Функция для подключения к базе данных
def connect_db():
    return sqlite3.connect(db_path)


# Функция для регистрации посещения
def register_visit(client_id=0):
    visit_date = datetime.date.today().isoformat()
    visit_time = datetime.datetime.now().time().strftime("%H:%M:%S")
    print("Путь к базе данных:", db_path)

    # Подключение к базе данных
    conn = connect_db()
    cursor = conn.cursor()

    # Вставка записи посещения
    cursor.execute('''
        INSERT INTO visits (client_id, visit_date, visit_time)
        VALUES (?, ?, ?)
    ''', (client_id, visit_date, visit_time))

    # Сохранение изменений и закрытие соединения
    conn.commit()
    conn.close()
    print("Посещение зарегистрировано автоматически")


# Вызов функции для регистрации посещения
register_visit()
