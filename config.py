import os

# Получаем путь к папке проекта
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Формируем динамический путь к базе данных
DATABASE_PATH = os.path.join(BASE_DIR, 'database', 'new_database_folder', 'gym_database.db')

# Путь к папке с QR-кодами
QR_CODES_DIR = os.path.join(BASE_DIR,  'qr_codes')
COMMON_FILES_DIR = os.path.join(BASE_DIR, 'Common Files')
