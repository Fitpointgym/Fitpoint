from flask import Flask, send_file, request, jsonify
import os
import sqlite3
from config import QR_CODES_DIR
from config import DATABASE_PATH  # Импортируем путь из config
app = Flask(__name__)

# Определяем путь к папке с QR-кодами
QR_CODES_FOLDER = QR_CODES_DIR

@app.route('/')
def home():
    return "Сервер работает! Добро пожаловать."

@app.route('/qr/<filename>')
def get_qr(filename):
    try:
        # Формируем полный путь к файлу
        file_path = os.path.join(QR_CODES_FOLDER, filename)
        link = f"https://Fitpoint.pythonanywhere.com/qr_codes/{filename}"
        print(f"Generated link: {link}")  # Для проверки ссылки в консоли
        return send_file(file_path)
    except FileNotFoundError:
        return "QR-код не найден!", 404

@app.route('/scan', methods=['GET'])
def scan():
    try:
        client_id = request.args.get('client_id')  # Получаем ID клиента
        visit_time = request.args.get('visit_time')  # Получаем время посещения

        # Разделяем дату и время
        visit_date, visit_time = visit_time.split(" ")

        # Подключаемся к базе данных
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        # Сохраняем данные в таблицу visits
        cursor.execute('''
            INSERT INTO visits (client_id, visit_date, visit_time)
            VALUES (?, ?, ?)
        ''', (client_id, visit_date, visit_time))

        # Сохраняем изменения
        conn.commit()
        conn.close()

        return jsonify({"status": "success", "message": "Посещение сохранено!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'))


