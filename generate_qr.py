import qrcode
import os
from config import QR_CODES_DIR

# Данные для QR-кода (например, URL для регистрации)
data = "https://Fitpoint.pythonanywhere.com/registration"
  # Замените на реальный URL или текст

# Создание QR-кода
qr = qrcode.QRCode(version=1, box_size=10, border=5)
qr.add_data(data)
qr.make(fit=True)

# Создание изображения QR-кода
img = qr.make_image(fill='black', back_color='white')

# Указываем путь к общей папке
output_path = os.path.join('CommonFiles', 'common_qr_code.png')

# Сохранение изображения в общей папке
img.save(output_path)

print(f"QR-код успешно сохранён по пути: {output_path}")

# Путь для сохранения QR-кодов
qr_folder = QR_CODES_DIR

if not os.path.exists(qr_folder):
    os.makedirs(qr_folder)

def generate_qr(client_id, last_name, first_name):
    # Текст для QR-кода (информация о клиенте)
    qr_text = f"ID: {client_id}\nФамилия: {last_name}\nИмя: {first_name}"

    # Генерация QR-кода
    qr = qrcode.make(qr_text)

    # Сохранение QR-кода с именем файла, содержащим ID клиента
    qr_path = os.path.join(qr_folder, f"client_{client_id}.png")
    qr.save(qr_path)
    return qr_path




