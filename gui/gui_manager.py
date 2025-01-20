from client_manager import record_visit, add_client, update_client, delete_client, find_client
import os
import tkinter as tk
from tkinter import messagebox
import qrcode
import sqlite3
from config import DATABASE_PATH  # Импортируем путь к базе данных
from datetime import datetime
from config import QR_CODES_DIR
import pywhatkit as kit  # Для отправки сообщений через WhatsApp

# Цвета для интерфейса
background_color = "#333333"
label_text_color = "#ffffff"
button_bg_color = "#4CAF50"
button_text_color = "white"

# Создание основного окна
root = tk.Tk()
root.title("Управление клиентами")
root.geometry("600x550")  # Увеличена высота для размещения всех элементов
root.configure(bg=background_color)

# Рамка для ввода данных
frame_top = tk.Frame(root, bg=background_color)
frame_top.pack(pady=10)

# Поля ввода данных
last_name_label = tk.Label(frame_top, text="Фамилия:", bg=background_color, fg=label_text_color)
last_name_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
last_name_entry = tk.Entry(frame_top)
last_name_entry.grid(row=0, column=1, padx=5, pady=5)

first_name_label = tk.Label(frame_top, text="Имя:", bg=background_color, fg=label_text_color)
first_name_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
first_name_entry = tk.Entry(frame_top)
first_name_entry.grid(row=1, column=1, padx=5, pady=5)

membership_type_label = tk.Label(frame_top, text="Тип абонемента:", bg=background_color, fg=label_text_color)
membership_type_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
membership_type_entry = tk.Entry(frame_top)
membership_type_entry.grid(row=2, column=1, padx=5, pady=5)

phone_number_label = tk.Label(frame_top, text="Номер телефона:", bg=background_color, fg=label_text_color)
phone_number_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
phone_number_entry = tk.Entry(frame_top)
phone_number_entry.grid(row=3, column=1, padx=5, pady=5)

add_button = tk.Button(frame_top, text="Добавить клиента", command=None, bg=button_bg_color, fg=button_text_color)
add_button.grid(row=4, column=0, columnspan=2, pady=10)

# Поле для ID клиента
client_id_label = tk.Label(frame_top, text="ID клиента для обновления:", bg=background_color, fg=label_text_color)
client_id_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")
client_id_entry = tk.Entry(frame_top)
client_id_entry.grid(row=5, column=1, padx=5, pady=5)

# Поле для ID клиента для удаления
delete_client_id_label = tk.Label(frame_top, text="ID клиента для удаления:", bg=background_color, fg=label_text_color)
delete_client_id_label.grid(row=6, column=0, padx=5, pady=5, sticky="w")
delete_client_id_entry = tk.Entry(frame_top)
delete_client_id_entry.grid(row=6, column=1, padx=5, pady=5)

delete_button = tk.Button(frame_top, text="Удалить клиента", command=None, bg=button_bg_color, fg=button_text_color)
delete_button.grid(row=7, column=0, columnspan=2, pady=5)

search_label = tk.Label(frame_top, text="Поиск клиента по имени:", bg=background_color, fg=label_text_color)
search_label.grid(row=8, column=0, padx=5, pady=5, sticky="w")
search_entry = tk.Entry(frame_top)
search_entry.grid(row=8, column=1, padx=5, pady=5)

find_button = tk.Button(frame_top, text="Найти клиента", command=None, bg=button_bg_color, fg=button_text_color)
find_button.grid(row=9, column=0, columnspan=2, pady=5)

visit_client_id_label = tk.Label(frame_top, text="ID для записи посещения:", bg=background_color, fg=label_text_color)
visit_client_id_label.grid(row=10, column=0, padx=5, pady=5, sticky="w")
visit_client_id_entry = tk.Entry(frame_top)
visit_client_id_entry.grid(row=10, column=1, padx=5, pady=5)

record_visit_button = tk.Button(frame_top, text="Записать посещение", command=None, bg=button_bg_color, fg=button_text_color)
record_visit_button.grid(row=11, column=0, columnspan=2, pady=5)

# Рамка для списка клиентов
frame_bottom = tk.Frame(root, bg=background_color)
frame_bottom.pack(pady=10)

client_listbox = tk.Listbox(frame_bottom, width=50, height=10)
client_listbox.pack(pady=5)

# Функции управления списком
def update_client_list():
    conn = sqlite3.connect(DATABASE_PATH)  # Используем динамический путь
    cursor = conn.cursor()
    cursor.execute("SELECT id, last_name, first_name, membership_type, phone_number, issue_date FROM clients")
    rows = cursor.fetchall()
    client_listbox.delete(0, tk.END)
    for row in rows:
        client_listbox.insert(tk.END, f"ID: {row[0]} | {row[1]} {row[2]} | {row[3]} | {row[4]} | {row[5]}")
    conn.close()

# Функция поиска клиента
def find_client_action():
    search_term = search_entry.get()
    if search_term:
        conn = sqlite3.connect(DATABASE_PATH)  # Используем динамический путь
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, last_name, first_name, membership_type, phone_number, issue_date 
            FROM clients 
            WHERE first_name LIKE ? OR last_name LIKE ?
        """, (f"%{search_term}%", f"%{search_term}%"))
        rows = cursor.fetchall()
        conn.close()
        client_listbox.delete(0, tk.END)
        if rows:
            for row in rows:
                client_listbox.insert(tk.END, f"ID: {row[0]} | {row[1]} {row[2]} | {row[3]} | {row[4]} | {row[5]}")
        else:
            messagebox.showinfo("Результат поиска", "Клиент не найден.")
    else:
        messagebox.showerror("Ошибка", "Пожалуйста, введите имя или фамилию для поиска.")

find_button.config(command=find_client_action)

# Функция добавления клиента и генерации QR-кода
def add_client_action():
    last_name = last_name_entry.get()
    first_name = first_name_entry.get()
    membership_type = membership_type_entry.get()
    phone_number = phone_number_entry.get()
    if last_name and first_name and membership_type and phone_number:
        conn = sqlite3.connect(DATABASE_PATH)  # Используем динамический путь
        cursor = conn.cursor()
        issue_datetime = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        cursor.execute("""
            INSERT INTO clients (last_name, first_name, membership_type, phone_number, issue_date) 
            VALUES (?, ?, ?, ?, ?)
        """, (last_name, first_name, membership_type, phone_number, issue_datetime))
        conn.commit()
        client_id = cursor.lastrowid
        conn.close()

        # Генерация QR-кода
        qr_data = f"{last_name}, {first_name}, {membership_type}, {phone_number}, {issue_datetime}"
        qr = qrcode.make(qr_data)

        qr_directory = QR_CODES_DIR

        qr_path = os.path.join(qr_directory, f"client_{client_id}.png")
        qr.save(qr_path)
        # Формирование ссылки на QR-код
        link_to_qr = f"https://Fitpoint.pythonanywhere.com/qr_codes/client_{client_id}.png"

        # Отправка сообщения через WhatsApp
        try:
            kit.sendwhatmsg_instantly(
                phone_number,
                f"Здравствуйте, {first_name}!\nВаш QR-код для посещений спортзала: {link_to_qr}",
                wait_time=10,
                tab_close=True
            )

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось отправить сообщение через WhatsApp: {e}")

        update_client_list()
        messagebox.showinfo("Успех", f"Клиент добавлен и QR-код сохранён по пути: {qr_path}")
    else:
        messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля.")

add_button.config(command=add_client_action)

# Функция удаления клиента и его QR-кода
def delete_client_action():
    client_id = delete_client_id_entry.get()
    if client_id:
        try:
            conn = sqlite3.connect(DATABASE_PATH)  # Используем динамический путь
            cursor = conn.cursor()
            cursor.execute("DELETE FROM clients WHERE id = ?", (int(client_id),))
            conn.commit()
            conn.close()

            qr_directory = QR_CODES_DIR

            qr_path = os.path.join(qr_directory, f"client_{client_id}.png")
            if os.path.exists(qr_path):
                os.remove(qr_path)

            update_client_list()
            messagebox.showinfo("Успех", f"Клиент с ID {client_id} удалён.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при удалении клиента: {e}")
    else:
        messagebox.showerror("Ошибка", "Пожалуйста, введите ID клиента для удаления.")

delete_button.config(command=delete_client_action)

# Загружаем список при запуске
update_client_list()

# Запуск основного цикла
root.mainloop()
