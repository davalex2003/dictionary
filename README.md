Бэкенд-часть проекта "Система для автоматической сборки языковых словарей"

Используется язык Python и СУБД PostgreSQL

Запуск:

1. Клонируем репозиторий
2. cd dictionary
3. docker compose up - для запуска docker-контейнера с БД
4. pip install -r requirements.txt - установка python библиотек
5. uvicorn app:app --host <ip> - запуск сервера
