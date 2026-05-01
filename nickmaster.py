import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import pyperclip
from PIL import Image, ImageTk
import os


class NickMasterPro:
    def __init__(self, root):
        self.root = root
        self.root.title("NickMaster Pro - Генератор никнеймов")
        self.root.geometry("700x600")
        self.root.minsize(600, 500)
        self.root.configure(bg='#1e1e1e')

        # Установка иконки
        self.setup_icon()

        # Настройки генерации
        self.length = tk.IntVar(value=10)
        self.use_uppercase = tk.BooleanVar(value=True)
        self.use_lowercase = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)

        # Символы для генерации
        self.symbols = "!@#$%&*_-.+?"

        # История генераций
        self.history = []

        # Создание интерфейса
        self.create_widgets()

        # Генерируем первый никнейм
        self.generate_nickname()

    def setup_icon(self):
        """Установка иконки приложения"""
        try:
            # Пробуем загрузить логотип
            if os.path.exists("resources/logo.ico"):
                self.root.iconbitmap("resources/logo.ico")
            elif os.path.exists("resources/logo.png"):
                logo = Image.open("resources/logo.png")
                logo = logo.resize((32, 32), Image.Resampling.LANCZOS)
                logo_tk = ImageTk.PhotoImage(logo)
                self.root.iconphoto(True, logo_tk)
        except:
            pass

    def create_widgets(self):
        """Создание интерфейса"""

        # Верхний баннер
        self.create_header()

        # Основной фрейм
        main_frame = tk.Frame(self.root, bg='#1e1e1e')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Блок сгенерированного никнейма
        self.create_nickname_display(main_frame)

        # Блок настроек
        self.create_settings(main_frame)

        # Блок с кнопками
        self.create_buttons(main_frame)

        # Блок истории
        self.create_history(main_frame)

        # Статус бар
        self.create_statusbar()

    def create_header(self):
        """Создание заголовка с логотипом"""
        header_frame = tk.Frame(self.root, bg='#2196F3', height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        # Загружаем логотип
        try:
            if os.path.exists("resources/logo.png"):
                logo_img = Image.open("resources/logo.png")
                logo_img = logo_img.resize((50, 50), Image.Resampling.LANCZOS)
                self.logo_tk = ImageTk.PhotoImage(logo_img)
                logo_label = tk.Label(header_frame, image=self.logo_tk, bg='#2196F3')
                logo_label.pack(side=tk.LEFT, padx=20, pady=15)
        except:
            pass

        # Название
        title_label = tk.Label(header_frame, text="NICKMASTER PRO",
                               bg='#2196F3', fg='white',
                               font=('Arial', 28, 'bold'))
        title_label.pack(side=tk.LEFT, padx=10)

        # Подзаголовок
        subtitle_label = tk.Label(header_frame, text="Генератор уникальных ников",
                                  bg='#2196F3', fg='#BBDEFB',
                                  font=('Arial', 12))
        subtitle_label.place(x=180, y=50)

    def create_nickname_display(self, parent):
        """Блок отображения сгенерированного никнейма"""
        display_frame = tk.Frame(parent, bg='#2d2d2d', relief=tk.RAISED, bd=2)
        display_frame.pack(fill=tk.X, pady=(0, 20))

        # Заголовок
        tk.Label(display_frame, text="✨ ТВОЙ НИКНЕЙМ ✨",
                 bg='#2d2d2d', fg='#FF9800',
                 font=('Arial', 14, 'bold')).pack(pady=(15, 5))

        # Поле с никнеймом
        self.nickname_var = tk.StringVar()
        self.nickname_entry = tk.Entry(display_frame, textvariable=self.nickname_var,
                                       font=('Courier New', 24, 'bold'),
                                       bg='#1e1e1e', fg='#4CAF50',
                                       justify='center', readonlybackground='#1e1e1e',
                                       relief=tk.SUNKEN, bd=3)
        self.nickname_entry.pack(fill=tk.X, padx=20, pady=(10, 20))
        self.nickname_entry.config(state='readonly')

        # Кнопка копирования под полем
        copy_btn = tk.Button(display_frame, text="📋 КОПИРОВАТЬ",
                             command=self.copy_to_clipboard,
                             bg='#FF9800', fg='white',
                             font=('Arial', 11, 'bold'),
                             activebackground='#e68900', cursor='hand2',
                             height=1, width=20)
        copy_btn.pack(pady=(0, 15))

    def create_settings(self, parent):
        """Блок настроек генерации"""
        settings_frame = tk.LabelFrame(parent, text="⚙️ НАСТРОЙКИ ГЕНЕРАЦИИ",
                                       bg='#2d2d2d', fg='white',
                                       font=('Arial', 12, 'bold'),
                                       relief=tk.RAISED, bd=2)
        settings_frame.pack(fill=tk.X, pady=(0, 20))

        # Длина никнейма
        length_frame = tk.Frame(settings_frame, bg='#2d2d2d')
        length_frame.pack(fill=tk.X, padx=15, pady=10)

        tk.Label(length_frame, text="Длина ника:", bg='#2d2d2d', fg='white',
                 font=('Arial', 11)).pack(side=tk.LEFT, padx=5)

        self.length_slider = tk.Scale(length_frame, from_=4, to=20,
                                      orient=tk.HORIZONTAL,
                                      variable=self.length,
                                      bg='#2d2d2d', fg='white',
                                      troughcolor='#2196F3',
                                      highlightbackground='#2d2d2d',
                                      length=300)
        self.length_slider.pack(side=tk.LEFT, padx=20)

        self.length_label = tk.Label(length_frame, text="10", bg='#2d2d2d',
                                     fg='#4CAF50', font=('Arial', 14, 'bold'))
        self.length_label.pack(side=tk.LEFT, padx=10)

        self.length_slider.configure(command=lambda x: self.length_label.config(text=str(int(x))))

        # Чекбоксы для символов
        chars_frame = tk.Frame(settings_frame, bg='#2d2d2d')
        chars_frame.pack(fill=tk.X, padx=15, pady=10)

        tk.Checkbutton(chars_frame, text="Заглавные буквы (A-Z)",
                       variable=self.use_uppercase,
                       bg='#2d2d2d', fg='white', selectcolor='#2d2d2d',
                       activebackground='#2d2d2d', activeforeground='white',
                       font=('Arial', 10)).pack(anchor=tk.W, pady=3)

        tk.Checkbutton(chars_frame, text="Строчные буквы (a-z)",
                       variable=self.use_lowercase,
                       bg='#2d2d2d', fg='white', selectcolor='#2d2d2d',
                       activebackground='#2d2d2d', activeforeground='white',
                       font=('Arial', 10)).pack(anchor=tk.W, pady=3)

        tk.Checkbutton(chars_frame, text="Цифры (0-9)",
                       variable=self.use_digits,
                       bg='#2d2d2d', fg='white', selectcolor='#2d2d2d',
                       activebackground='#2d2d2d', activeforeground='white',
                       font=('Arial', 10)).pack(anchor=tk.W, pady=3)

        tk.Checkbutton(chars_frame, text="Спецсимволы (!@#$%&*_-.+?)",
                       variable=self.use_symbols,
                       bg='#2d2d2d', fg='white', selectcolor='#2d2d2d',
                       activebackground='#2d2d2d', activeforeground='white',
                       font=('Arial', 10)).pack(anchor=tk.W, pady=3)

    def create_buttons(self, parent):
        """Блок кнопок управления"""
        buttons_frame = tk.Frame(parent, bg='#1e1e1e')
        buttons_frame.pack(fill=tk.X, pady=(0, 20))

        # Кнопка генерации
        generate_btn = tk.Button(buttons_frame, text="🎲 СГЕНЕРИРОВАТЬ",
                                 command=self.generate_nickname,
                                 bg='#4CAF50', fg='white',
                                 font=('Arial', 14, 'bold'),
                                 activebackground='#45a049', cursor='hand2',
                                 height=2)
        generate_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        # Кнопка копирования
        copy_btn2 = tk.Button(buttons_frame, text="📋 КОПИРОВАТЬ",
                              command=self.copy_to_clipboard,
                              bg='#2196F3', fg='white',
                              font=('Arial', 14, 'bold'),
                              activebackground='#1976D2', cursor='hand2',
                              height=2)
        copy_btn2.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        # Кнопка очистки истории
        clear_btn = tk.Button(buttons_frame, text="🗑️ ОЧИСТИТЬ ИСТОРИЮ",
                              command=self.clear_history,
                              bg='#f44336', fg='white',
                              font=('Arial', 12, 'bold'),
                              activebackground='#d32f2f', cursor='hand2',
                              height=2)
        clear_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

    def create_history(self, parent):
        """Блок истории генераций"""
        history_frame = tk.LabelFrame(parent, text="📜 ИСТОРИЯ ГЕНЕРАЦИЙ",
                                      bg='#2d2d2d', fg='white',
                                      font=('Arial', 11, 'bold'),
                                      relief=tk.RAISED, bd=2)
        history_frame.pack(fill=tk.BOTH, expand=True)

        # Создаём список с прокруткой
        list_frame = tk.Frame(history_frame, bg='#2d2d2d')
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.history_listbox = tk.Listbox(list_frame,
                                          bg='#1e1e1e',
                                          fg='#4CAF50',
                                          font=('Courier New', 11),
                                          selectbackground='#2196F3',
                                          yscrollcommand=scrollbar.set,
                                          height=5)
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.history_listbox.yview)

        # Двойной клик для копирования из истории
        self.history_listbox.bind('<Double-Button-1>', self.copy_from_history)

    def create_statusbar(self):
        """Статусная строка"""
        self.statusbar = tk.Label(self.root, text="✅ Готов к работе | Нажми 'Сгенерировать'",
                                  bd=1, relief=tk.SUNKEN, anchor=tk.W,
                                  bg='#2d2d2d', fg='#aaa')
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)

    def generate_nickname(self):
        """Генерация случайного никнейма"""

        # Проверяем, что выбран хотя бы один тип символов
        if not (self.use_uppercase.get() or self.use_lowercase.get() or
                self.use_digits.get() or self.use_symbols.get()):
            messagebox.showwarning("Ошибка", "Выберите хотя бы один тип символов!")
            return

        # Формируем пул символов
        chars = ""
        if self.use_uppercase.get():
            chars += string.ascii_uppercase  # A-Z
        if self.use_lowercase.get():
            chars += string.ascii_lowercase  # a-z
        if self.use_digits.get():
            chars += string.digits  # 0-9
        if self.use_symbols.get():
            chars += self.symbols  # спецсимволы

        # Генерируем никнейм
        length = self.length.get()
        nickname = ''.join(random.choice(chars) for _ in range(length))

        # Обновляем отображение
        self.nickname_var.set(nickname)

        # Добавляем в историю
        self.history.insert(0, nickname)
        if len(self.history) > 20:  # Ограничиваем историю 20 записями
            self.history.pop()

        self.update_history_display()

        # Обновляем статус
        self.statusbar.config(text=f"✅ Сгенерирован никнейм длины {length}")

        # Анимация (мигание)
        self.animate_generation()

    def animate_generation(self):
        """Простая анимация при генерации"""
        original_color = self.nickname_entry.cget('fg')
        self.nickname_entry.config(fg='#FF9800')
        self.root.after(200, lambda: self.nickname_entry.config(fg=original_color))

    def copy_to_clipboard(self):
        """Копирование никнейма в буфер обмена"""
        nickname = self.nickname_var.get()
        if nickname:
            pyperclip.copy(nickname)
            self.statusbar.config(text=f"📋 Скопировано: {nickname}")

            # Визуальный фидбек
            self.statusbar.config(bg='#4CAF50')
            self.root.after(1500, lambda: self.statusbar.config(bg='#2d2d2d'))
        else:
            messagebox.showwarning("Ошибка", "Нет никнейма для копирования!")

    def copy_from_history(self, event):
        """Копирование из истории при двойном клике"""
        selection = self.history_listbox.curselection()
        if selection:
            nickname = self.history_listbox.get(selection[0])
            pyperclip.copy(nickname)
            self.statusbar.config(text=f"📋 Из истории скопировано: {nickname}")

    def update_history_display(self):
        """Обновление отображения истории"""
        self.history_listbox.delete(0, tk.END)
        for nick in self.history:
            self.history_listbox.insert(tk.END, nick)

    def clear_history(self):
        """Очистка истории"""
        if messagebox.askyesno("Подтверждение", "Очистить всю историю?"):
            self.history = []
            self.update_history_display()
            self.statusbar.config(text="🗑️ История очищена")


def main():
    root = tk.Tk()
    app = NickMasterPro(root)
    root.mainloop()


if __name__ == "__main__":
    main()