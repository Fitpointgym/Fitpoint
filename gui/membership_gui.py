import tkinter as tk
from tkinter import messagebox
import sqlite3
from config import DATABASE_PATH
import qrcode
import os
from datetime import datetime

def save_membership():
    last_name = last_name_entry.get()
    first_name = first_name_entry.get()
    membership_type = membership_type_entry.get()
    date_of_issue = date_of_issue_entry.get()  # Получаем дату оформления

    if not last_name or not first_name or not membership_type or not date_of_issue:
        messagebox.showwarning("Warning", "Пожалуйста, заполните все поля!")
        return

    # Сохраняем данные в базу данных
    db_path = DATABASE_PATH  # Указываем путь к базе данных
    conn = sqlite3.connect(DATABASE_PATH)  # Используем этот путь для подключения
    cursor = conn.cursor()
    cursor.execute("INSERT INTO clients (last_name, first_name, membership_type, date_of_issue) VALUES (?, ?, ?, ?)",
                   (last_name, first_name, membership_type, date_of_issue))
    conn.commit()
    conn.close()

    # Генерируем QR-код
    qr_data = f"{last_name}, {first_name}, {membership_type}, {date_of_issue}"
    qr = qrcode.make(qr_data)
    qr.save('qr_code.png')

    messagebox.showinfo("Success", "Данные успешно сохранены и QR-код сгенерирован!")

# Создаем основное окно
root = tk.Tk()
root.title("Графический интерфейс абонемента")

# Поля для ввода данных
tk.Label(root, text="Фамилия:").pack()
last_name_entry = tk.Entry(root)
last_name_entry.pack()

tk.Label(root, text="Имя:").pack()
first_name_entry = tk.Entry(root)
first_name_entry.pack()

tk.Label(root, text="Тип абонемента:").pack()
membership_type_entry = tk.Entry(root)
membership_type_entry.pack()

tk.Label(root, text="Дата оформления (ДД.ММ.ГГГГ):").pack()  # Новая метка для даты
date_of_issue_entry = tk.Entry(root)  # Новое поле для ввода даты
date_of_issue_entry.pack()

# Кнопка для сохранения данных
save_button = tk.Button(root, text="Сохранить", command=save_membership)
save_button.pack()

# Запускаем главный цикл
root.mainloop()


