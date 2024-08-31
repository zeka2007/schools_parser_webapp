# Общая информация
Backend для Telegram Mini App ([@schools_helper_bot](https://t.me/schools_helper_bot)). Имеете те же возможности что и бот, однако является более комфортным с точки зрения использования.

# Возможности
- [x] Добавление, изменение, удаление аккаунтов SCHOOLS.BY
- [x] Добавление, изменение, удаление виртуальных дневников
- [x] Создание, изменение, удаление предметов и отметок для виртуальных дневников
- [x] Экспорт данных в Exel
- [x] Инструменты для анализа (анализ четвртей, калькулятор отметок, способы исправления и другие)
- [x] Все возможности бота

**Возможности, которые находятся в процессе разработки:**

- [ ] Копирование информации из дневников

# Установка 
Backend часть может работать отдельно от бота, однако для расшифровки сообщений с Frontend необходимо указать токен бота в `.env` файле. 

1. Для запуска нужно установить [Python 3](https://www.python.org/) и [PostgreSQL](https://www.postgresql.org/)

2. Затем установить зависимости:
    > pip install -r requirements.txt

3. Создать файл с именем `.env` и внести в него необходимые данные или заполнить файл `config.py`

4. Создать базу данных:
    > python3 create_db.py
