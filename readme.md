# HSE Casino

## Обзор

HSE Casino - это веб-приложение, представляющее собой онлайн-казино с различными играми. Проект создан в рамках первого модуля Python в НИУ ВШЭ.

## Фичи

- Европейский блэкджек
- Динамическое обновление игры через jQuery и AJAX
- РАКЭТКААААА
- СЛОТИКИ

## Устновка

### Пререквизиты

- Python 3.12
- pip (Python package installer)

### Шаги

1. Клонируйте репозиторий:
    ```sh
    git clone https://github.com/4e6yPeK48/hse-casino
    cd hse-casino
    ```

2. Создайте виртуальное окружение:
    ```sh
    python -m venv venv
    ```

3. Активируйте виртуальное окружение:
    - Windows:
        ```sh
        venv\Scripts\activate
        ```
    - macOS/Linux:
        ```sh
        source venv/bin/activate
        ```

4. Установите зависимости:
    ```sh
    pip install -r requirements.txt
    ```

5. Создайте базу данных:
    ```sh
    python
    >>> from app import db
    >>> db.create_all()
    >>> exit()
    ```
   
6. Добавьте .env файл в корень проекта:
    ```sh
   FLASK_APP=app.py
   FLASK_ENV=development/production
   SECRET_KEY=YourSecretKey
   SQLALCHEMY_DATABASE_URI = 'YourDatabaseURI'
   SQLALCHEMY_TRACK_MODIFICATIONS = False

7. Запустите приложение:
    ```sh
    python app.py
    ```

## Использование

- Перейти на `http://localhost:5000`
- Игры в навбаре
- А ЕЩЕ ЕСТЬ РАКЭТКА И СЛОТИКИ

## Стек технологий
- **Backend**:
  - ЯП: Python
  - Веб-фреймворк: Flask
  - ORM: SQLAlchemy

- **Frontend**:
  - Язык программирования: JavaScript
  - Библиотека: jQuery

- **База данных**:
  - Любая реляционная БД, поддерживаемая SQLAlchemy (изначально MariaDB)

- **Прочее**:
  - HTML и CSS для разметки и стилей веб-страниц
  - Flask-WTF для работы с формами (например, `RegistrationForm`, `LoginForm`)
  - Flask-SQLAlchemy для интеграции SQLAlchemy с Flask
  - Flask-Session для управления сессиями пользователей

## Лицензия

Проект под MIT License.
