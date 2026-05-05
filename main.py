import tkinter as tk
import json
import os

# --- Глобальные переменные ---
DATA_FILE = "movies.json"
movies = []
current_filter_genre = ""
current_filter_year = ""

# --- Функции для работы с данными (JSON) ---
def load_data():
    """Загружает фильмы из файла при запуске программы."""
    global movies
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                movies = json.load(f)
        except Exception as e:
            print("Ошибка чтения файла:", e)
            movies = []
    else:
        print("Файл данных не найден. Будет создан новый.")

def save_data():
    """Сохраняет список фильмов в файл."""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(movies, f, ensure_ascii=False, indent=2)

# --- Функции для проверки ввода (валидация) ---
def is_valid_year(year_str):
    """Проверяет, что год — это число в разумном диапазоне."""
    try:
        year = int(year_str)
        return 1890 < year < 2030
    except ValueError:
        return False

def is_valid_rating(rating_str):
    """Проверяет, что рейтинг — это число от 0 до 10."""
    try:
        rating = float(rating_str)
        return 0 <= rating <= 10
    except ValueError:
        return False

# --- Функции для обновления списка на экране ---
def update_listbox_display():
    """
    Очищает список на экране и заново выводит все фильмы,
    которые подходят под текущие фильтры.
    """
    # 1. Очистить текущее содержимое списка
    movie_listbox.delete(0, tk.END)
    
    # 2. Получить отфильтрованный список
    filtered_movies = filter_movies()
    
    # 3. Если фильмов нет, вывести сообщение
    if not filtered_movies:
        movie_listbox.insert(tk.END, "--- Фильмов не найдено ---")
        return
    
    # 4. Вывести каждый фильм в виде одной строки с разделителями
    for m in filtered_movies:
        line = f"{m['title']} | {m['genre']} | {m['year']} | Рейтинг: {m['rating']}"
        movie_listbox.insert(tk.END, line)

# --- Логика фильтрации ---
def filter_movies():
    """
    Возвращает новый список фильмов,
    отфильтрованный по жанру и/или году.
    """
    filtered = movies.copy()
    
    # Фильтр по жанру (если он задан)
    if current_filter_genre:
        filtered = [m for m in filtered if current_filter_genre.lower() in m["genre"].lower()]
    
    # Фильтр по году (если он задан и является числом)
    if current_filter_year.isdigit():
        year_int = int(current_filter_year)
        filtered = [m for m in filtered if m["year"] == year_int]
    
    return filtered

# --- Логика добавления фильма ---
def add_movie():
    """Берем данные из полей, проверяем их и добавляем в список."""
    # Получаем текст из полей ввода
    title = title_entry.get().strip()
    genre = genre_entry.get().strip()
    year = year_entry.get().strip()
    rating = rating_entry.get().strip()
    
    # Проверка 1: Все ли поля заполнены?
    if not (title and genre and year and rating):
        print("Ошибка: Заполните все поля!")
        return
    
    # Проверка 2: Корректный ли год?
    if not is_valid_year(year):
        print("Ошибка: Год должен быть числом (например, 2010)!")
        return
    
    # Проверка 3: Корректный ли рейтинг?
    if not is_valid_rating(rating):
        print("Ошибка: Рейтинг должен быть числом от 0 до 10!")
        return

    # Если все проверки пройдены, создаем словарь фильма
    new_movie = {
        "title": title,
        "genre": genre,
        "year": int(year),
        "rating": float(rating)
    }
    
    # Добавляем в глобальный список и сохраняем в файл
    movies.append(new_movie)
    save_data()
    
    # Обновляем список на экране и очищаем поля ввода
    update_listbox_display()
    
    title_entry.delete(0, tk.END)
    genre_entry.delete(0, tk.END)
    year_entry.delete(0, tk.END)
    rating_entry.delete(0, tk.END)

# --- Логика применения фильтров ---
def apply_filters():
    """Берем текст из полей фильтра и обновляем список."""
    global current_filter_genre, current_filter_year
    
    current_filter_genre = filter_genre_entry.get()
    current_filter_year = filter_year_entry.get()
    
    update_listbox_display()

def reset_filters():
    """Очищаем поля фильтра и сбрасываем глобальные переменные."""
    global current_filter_genre, current_filter_year
    
    current_filter_genre = ""
    current_filter_year = ""
    
    filter_genre_entry.delete(0, tk.END)
    filter_year_entry.delete(0, tk.END)
    
    update_listbox_display()


# --- Главная часть: создание окна и виджетов ---
if __name__ == "__main__":

    # Создаем главное окно
    root = tk.Tk()
    root.title("Movie Library")
    
    # Загружаем данные перед созданием интерфейса
    load_data()


    # --- Блок 1: Поля для ввода нового фильма ---
    input_frame = tk.Frame(root)
    input_frame.pack(padx=10, pady=5, fill="x")

    tk.Label(input_frame, text="Название:").grid(row=0, column=0, sticky="e")
    title_entry = tk.Entry(input_frame)
    title_entry.grid(row=0, column=1, sticky="we", padx=2)

    tk.Label(input_frame, text="Жанр:").grid(row=1, column=0, sticky="e")
    genre_entry = tk.Entry(input_frame)
    genre_entry.grid(row=1, column=1, sticky="we", padx=2)

    tk.Label(input_frame, text="Год:").grid(row=2, column=0, sticky="e")
    year_entry = tk.Entry(input_frame)
    year_entry.grid(row=2, column=1, sticky="we", padx=2)

    tk.Label(input_frame, text="Рейтинг:").grid(row=3, column=0, sticky="e")
    rating_entry = tk.Entry(input_frame)
    rating_entry.grid(row=3, column=1, sticky="we", padx=2)


     # --- Блок 2: Кнопки действий (Добавить) ---
    button_frame = tk.Frame(root)
    button_frame.pack(pady=5, fill="x")
     
    add_button = tk.Button(button_frame, text="Добавить фильм", command=add_movie)
    add_button.pack(side="left", padx=5)


     # --- Блок 3: Поля для фильтрации ---
    filter_frame = tk.Frame(root)
    filter_frame.pack(pady=5, fill="x")
     
    tk.Label(filter_frame, text="Жанр:").pack(side="left")
    filter_genre_entry = tk.Entry(filter_frame)
    filter_genre_entry.pack(side="left", padx=2)
     
    tk.Label(filter_frame, text="Год:").pack(side="left")
    filter_year_entry = tk.Entry(filter_frame)
    filter_year_entry.pack(side="left", padx=2)
     
    apply_btn = tk.Button(filter_frame, text="Применить", command=apply_filters)
    apply_btn.pack(side="left", padx=5)
     
    reset_btn = tk.Button(filter_frame, text="Сбросить", command=reset_filters)
    reset_btn.pack(side="left")


     # --- Блок 4: Список для вывода фильмов (Listbox) ---
    list_frame = tk.Frame(root)
    list_frame.pack(padx=10, pady=10, fill="both", expand=True)
     
    movie_listbox = tk.Listbox(list_frame, width=80, height=15)
    movie_listbox.pack(side="left", fill="both", expand=True)
     
     # Добавляем скроллбар к списку (это обязательная часть для Listbox!)
    scrollbar = tk.Scrollbar(list_frame)
    scrollbar.pack(side="right", fill="y")
     
    movie_listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=movie_listbox.yview)


     # Выводим фильмы при запуске программы
    update_listbox_display()


    root.mainloop()
