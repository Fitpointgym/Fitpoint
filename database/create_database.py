import sqlite3
from config import DATABASE_PATH  # Импортируем путь из config

# Подключение к базе данных (или создание, если её ещё нет)
conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()

# Создаём таблицу для клиентов, если её ещё нет
cursor.execute('''
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        last_name TEXT NOT NULL,
        first_name TEXT NOT NULL,
        membership_type TEXT NOT NULL,
        issue_date TEXT NOT NULL
    )
''')

# Создаём таблицу для посещений, если её ещё нет
cursor.execute('''
    CREATE TABLE IF NOT EXISTS visits (
        visit_id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER,
        visit_date TEXT,
        visit_time TEXT,
        FOREIGN KEY (client_id) REFERENCES clients(id)
    )
''')

# Сохранение изменений и закрытие подключения
conn.commit()
conn.close()

print("Таблицы успешно созданы.")
