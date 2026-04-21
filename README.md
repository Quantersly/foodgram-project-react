# Foodgram — Продуктовый помощник

**Автор проекта:** Алексей Лоскутников (В рамках курса от Яндекс Практикума "Python-разработчик")

### Телеграм: https://t.me/AlexeyLoskutnikov07

### **Демо-версия:** https://loskutnikov-diplom.site

Проект «Foodgram» — это онлайн-сервис и социальная сеть для обмена рецептами. Пользователи могут публиковать рецепты, подписываться на авторов, добавлять понравившиеся блюда в «Избранное», а перед походом в магазин формировать и скачивать список покупок в формате PDF.

## 🚀 Технологический стек
*   **Backend:** Python 3.9, Django, Django REST Framework
*   **Frontend:** React (JavaScript)
*   **Database:** PostgreSQL
*   **Infrastructure:** Docker, Docker Compose, Nginx (TLS/SSL)
*   **CI/CD:** GitHub Actions (автоматический запуск тестов, сборка Docker-образов и деплой на сервер)

---

## 🛠 Установка и запуск (Local/No SSL)

Для локального запуска или развертывания без домена и SSL:

1.  **Клонируйте репозиторий:**
    ```bash
    git clone https://github.com/Quantersly/foodgram-project-react.git
    ```

2.  **Настройте окружение:**
    Создайте файл `infra/.env` на основе примера:
    ```bash
    cp infra/.env.example infra/.env
    ```

3.  **Запустите контейнеры:**
    ```bash
    cd infra/
    docker compose up -d
    ```

4.  **Выполните миграции и соберите статику:**
    ```bash
    docker compose exec backend python manage.py migrate
    docker compose exec backend python manage.py collectstatic --no-input
    ```

Проект будет доступен по адресу: `http://localhost/`

---

## 🔒 Развертывание на сервере (Production & TLS/SSL)

Проект настроен на работу с доменом и сертификатами Let's Encrypt.

1.  **Конфигурация Nginx:**
    Используйте шаблон из `infra/nginx.tls.conf.example`. Замените `<your_domain>` на ваш реальный домен.
2.  **Сертификаты:**
    Сертификаты пробрасываются в контейнер Nginx через volume `/etc/letsencrypt/`.
3.  **CI/CD:**
    При пуше в ветку `master` GitHub Actions автоматически соберет образы и обновит проект на сервере.

---

## 📋 Команды управления

*   **Наполнение базы ингредиентами:**
    ```bash
    docker compose exec backend python manage.py import_csv
    ```
*   **Создание суперпользователя:**
    ```bash
    docker compose exec backend python manage.py createsuperuser
    ```

---

## 🔧 CI/CD Workflow
Настроен пайплайн в `.github/workflows/main.yml`:
1.  **Tests:** Проверка кода на соответствие PEP8.
2.  **Build and Push:** Сборка backend/frontend образов и их пуш в Docker Hub.
3.  **Deploy:** Автоматическое обновление конфигурации на сервере по SSH.
4.  **Send Message:** Уведомление в Telegram об успешном деплое.

---

## Actions secrets:
```
ALLOWED_HOSTS
BASE_URL
DB_ENGINE
DB_HOST
DB_NAME
DB_PORT
DEBUG
DOCKER_PASSWORD
DOCKER_USERNAME
HOST
POSTGRES_PASSWORD
POSTGRES_USER
SECRET_KEY
SSH_KEY
SSH_PASSPHRASE #Добавляем по мере надобности
TELEGRAM_TO
TELEGRAM_TOKEN
USER
```
