# База знаний технического анализа

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Django](https://img.shields.io/badge/django-4.x-green)
![License](https://img.shields.io/badge/license-MIT-brightgreen)
![Status](https://img.shields.io/badge/status-active-success)

Добро пожаловать в **Базу знаний технического анализа**! 🎓 Это интерактивное веб-приложение, созданное для изучения и тестирования знаний о технических индикаторах финансового анализа. Управляйте индикаторами, изучайте их формулы в формате LaTeX и проверяйте свои навыки с помощью увлекательного квиза!

---

## Описание проекта

Приложение состоит из трех ключевых страниц:

1. **Главная страница**
   Приветствует пользователей с кратким описанием и ссылками на основные разделы.

2. **Технические индикаторы**
   Позволяет просматривать, добавлять, редактировать и удалять индикаторы. Каждый индикатор включает:
   - Название
   - Описание
   - Формулу (отображается в LaTeX, например, \( RSI = 100 - \frac{100}{1 + RS} \))
   - Рекомендацию

3. **Квиз**
   Интерактивный тест из 10 вопросов с выбором ответа, включая вопросы о формулах, описаниях и рекомендациях. После завершения отображается результат (например, "7/10 — Отлично!") с цветной разметкой (зеленый/желтый/красный) для ответов.

### Используемые технологии и решения

- **Django**: Основной фреймворк для серверной логики, маршрутизации и работы с базой данных.
- **SQLite**: Легковесная база данных для хранения индикаторов (модель `TechnicalIndicator`).
- **Materialize CSS**: Современный, адаптивный фронтенд с модальными окнами и карточками.
- **MathJax**: Рендеринг математических формул в LaTeX для профессионального отображения (например, \( EMA_t = P_t \cdot k + EMA_{t-1} \cdot (1 - k) \)).
- **Django Messages**: Уведомления о действиях (добавление, редактирование, ошибки).
- **Session Framework**: Хранение состояния квиза (вопросы, ответы, результаты).

Проект следует принципам чистого кода, имеет адаптивный дизайн и интуитивно понятный интерфейс.

---

## Как запустить проект

### Требования

- Python 3.8 или выше
- pip (менеджер пакетов Python)
- Git (для клонирования репозитория)

### Установка

1. **Клонируйте репозиторий**:
    ```bash
    git clone <repository-url>
    cd django-practise
    ```

2. Создайте и активируйте виртуальное окружение
    ```bash
    python -m venv venv
    source venv/bin/activate  # На Windows: venv\Scripts\activate
    ```

3. Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```

4. Запустите сервер:
    ```bash
    python manage.py runserver
    ```
