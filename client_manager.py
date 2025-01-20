import os
import sqlite3
from config import DATABASE_PATH
from datetime import datetime
def connect_db():
    return sqlite3.connect(DATABASE_PATH)  # Подключение с использованием пути из конфигурации

# Устанавливаем путь к базе данных
db_path = DATABASE_PATH

def connect_db():
    """Подключение к базе данных."""
    return sqlite3.connect(DATABASE_PATH)

def add_client(last_name, first_name, membership_type):
    """Добавление нового клиента в базу данных."""
    conn = connect_db()
    cursor = conn.cursor()

    # Устанавливаем текущую дату как дату покупки абонемента
    issue_date = datetime.now().date().isoformat()

    cursor.execute('''
        INSERT INTO clients (last_name, first_name, membership_type, issue_date)
        VALUES (?, ?, ?, ?)
    ''', (last_name, first_name, membership_type, issue_date))

    conn.commit()
    conn.close()
    print(f"Клиент {first_name} {last_name} добавлен.")

def update_client(client_id, last_name, first_name, membership_type):
    """Обновление информации о клиенте по его ID."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE clients
        SET last_name = ?, first_name = ?, membership_type = ?
        WHERE id = ?
    ''', (last_name, first_name, membership_type, client_id))

    conn.commit()
    conn.close()
    print(f"Клиент с ID {client_id} обновлён.")

def delete_client(client_id):
    """Удаление клиента из базы данных по его ID."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
        DELETE FROM clients
        WHERE id = ?
    ''', (client_id,))

    conn.commit()
    conn.close()
    print(f"Клиент с ID {client_id} удалён.")

def find_client(search_term):
    """Поиск клиента по фамилии или имени."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM clients
        WHERE last_name LIKE ? OR first_name LIKE ?
    ''', (f'%{search_term}%', f'%{search_term}%'))

    results = cursor.fetchall()
    conn.close()

    if results:
        print("Найденные клиенты:")
        for row in results:
            print(row)
    else:
        print("Клиенты не найдены.")


# Функция для записи посещения клиента
def record_visit(client_id):
    # Подключаемся к базе данных
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Получаем текущие дату и время
    visit_date = datetime.now().strftime("%Y-%m-%d")
    visit_time = datetime.now().strftime("%H:%M:%S")

    # Вставляем запись о посещении в таблицу visits
    cursor.execute('''
        INSERT INTO visits (client_id, visit_date, visit_time)
        VALUES (?, ?, ?)
    ''', (client_id, visit_date, visit_time))

    # Сохраняем изменения и закрываем подключение
    conn.commit()
    conn.close()

    print(f"Посещение клиента с ID {client_id} успешно записано.")

