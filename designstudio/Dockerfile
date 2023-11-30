# официальный образ Python в качестве родительского образа
FROM python:3.10

# рабочая директория
WORKDIR /code

# Копируем файлы зависимостей
COPY requirements.txt .

# Уставливаем все зависимости
RUN pip install --no-cache-dir -r requirements.txt

# содержимое локального каталога designstudio в рабочей директории контейнера
COPY designstudio /code/

# порт 8000 для доступа к вашему приложению вне контейнера
EXPOSE 8080

# переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# сервер приложений Django при запуске контейнера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
