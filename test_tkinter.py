import tkinter as tk

def main():
    root = tk.Tk()  # Создаем основное окно
    root.title("Тест Tkinter")  # Устанавливаем заголовок окна
    label = tk.Label(root, text="Tkinter работает!")  # Создаем метку с текстом
    label.pack()  # Размещаем метку в окне
    root.mainloop()  # Запускаем главный цикл приложения

if __name__ == "__main__":
    main()
