import sqlite3
from config import DATABASE_PATH  # Импортируем путь к базе данных
# Подключаемся к базе данных
conn = sqlite3.connect(DATABASE_PATH)  # Используем динамический путь
cursor = conn.cursor()

# Добавляем новое поле в таблицу clients
cursor.execute('ALTER TABLE clients ADD COLUMN phone_number TEXT')

# Сохраняем изменения и закрываем соединение
conn.commit()
conn.close()

print("Поле phone_number успешно добавлено в таблицу clients!")
