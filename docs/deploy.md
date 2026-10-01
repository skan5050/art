# Размещение двух сайтов на VPS

Инструкция для обычного VPS с Ubuntu 22.04/24.04 (например, Timeweb Cloud, Selectel, REG.RU).
Docker не нужен. Каждый сайт ставится **отдельной установкой**: у него своя папка с кодом, своё виртуальное окружение, своя база, медиатека, пользователь системы, сервис и домен. Так выполняется раздел 1.1 ТЗ.

Если оба сайта стоят на одном сервере, процессы, данные и доступы у них разделены. Но сам сервер остаётся общей точкой отказа. Для полной независимости от аварий нужны два сервера — это отдельное решение.

Ниже команды для сайта A (МираМе). Для сайта D повторите их, заменив `mirame` на `holstory`, `a` на `d` и домен.

## 1. Подготовка сервера (один раз)

```bash
sudo apt update && sudo apt install -y python3-venv python3-dev nginx certbot python3-certbot-nginx git
```

## 2. Установка сайта

```bash
sudo adduser --system --group --home /srv/mirame mirame
sudo -u mirame git clone https://github.com/skan5050/art.git /srv/mirame/app
cd /srv/mirame/app
sudo -u mirame python3 -m venv /srv/mirame/venv
sudo -u mirame /srv/mirame/venv/bin/pip install -r requirements.txt
```

Создайте `/srv/mirame/app/.env` (права `600`, владелец `mirame`):

```ini
SITE_THEME=a
SECRET_KEY=<длинная случайная строка: python3 -c "import secrets;print(secrets.token_urlsafe(50))">
DEBUG=0
ALLOWED_HOSTS=mirame.ru,www.mirame.ru
CSRF_TRUSTED_ORIGINS=https://mirame.ru
ADMIN_PATH=admin
DATA_DIR=/srv/mirame/var
EMAIL_HOST=smtp.yandex.ru
EMAIL_PORT=465
EMAIL_USE_SSL=1
EMAIL_USE_TLS=0
EMAIL_HOST_USER=noreply@mirame.ru
EMAIL_HOST_PASSWORD=<пароль приложения>
DEFAULT_FROM_EMAIL=noreply@mirame.ru
```

У второго сайта обязательно свой `SECRET_KEY`: от него зависят сессии, CSRF и проверка API-ключей. Ключ A не должен подходить к D.

```bash
sudo -u mirame /srv/mirame/venv/bin/python manage.py migrate
sudo -u mirame /srv/mirame/venv/bin/python manage.py collectstatic --noinput
sudo -u mirame /srv/mirame/venv/bin/python manage.py seed_site
sudo -u mirame /srv/mirame/venv/bin/python manage.py import_cities
sudo -u mirame /srv/mirame/venv/bin/python manage.py createsuperuser
```

По умолчанию используется SQLite. Для небольшого каталога его достаточно, а резервное копирование сводится к копированию файлов. Если нужен PostgreSQL, заведите отдельную базу и отдельного пользователя для каждого сайта, установите `psycopg[binary]` и задайте `DB_ENGINE=postgres` и `DB_*`.

## 3. Сервис приложения (systemd)

`/etc/systemd/system/mirame.service`:

```ini
[Unit]
Description=MiraMe site
After=network.target

[Service]
User=mirame
Group=mirame
WorkingDirectory=/srv/mirame/app
ExecStart=/srv/mirame/venv/bin/gunicorn artsite.wsgi:application --workers 3 --bind unix:/run/mirame/gunicorn.sock --timeout 120
RuntimeDirectory=mirame
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload && sudo systemctl enable --now mirame
```

## 4. Nginx и HTTPS

`/etc/nginx/sites-available/mirame`:

```nginx
server {
    listen 80;
    server_name mirame.ru www.mirame.ru;
    return 301 https://mirame.ru$request_uri;
}

server {
    listen 443 ssl http2;
    server_name www.mirame.ru;
    # сертификаты пропишет certbot
    return 301 https://mirame.ru$request_uri;
}

server {
    listen 443 ssl http2;
    server_name mirame.ru;
    client_max_body_size 45m;               # вложения форм и импорт фото

    location /static/ { alias /srv/mirame/var/static/; expires 30d; access_log off; }
    location /media/  { alias /srv/mirame/var/media/;  expires 30d; access_log off;
                        location ~* \.(php|py|html?|svg|js)$ { deny all; } }
    # /srv/mirame/var/private/ наружу не раздается: вложения заявок и оригиналы импорта

    location / {
        proxy_pass http://unix:/run/mirame/gunicorn.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/mirame /etc/nginx/sites-enabled/
sudo certbot --nginx -d mirame.ru -d www.mirame.ru
sudo nginx -t && sudo systemctl reload nginx
```

Выберите одну основную версию хоста: с `www` или без. Остальные версии перенаправляются на неё кодом 301 (раздел 12.3 ТЗ). Этот же адрес укажите в админке: «Общие настройки → Основной адрес сайта».

**Тестовый сайт** закройте паролем (`auth_basic` в nginx), а не только файлом robots.txt.

## 5. Резервные копии и проверка восстановления

Резервная копия сайта — это одна папка `/srv/mirame/var` (база SQLite, медиатека, закрытые файлы) плюс файл `.env`. У каждого сайта свой архив.

`/etc/cron.daily/mirame-backup`:

```bash
#!/bin/sh
set -e
D=/srv/backups/mirame; mkdir -p $D
sqlite3 /srv/mirame/var/db.sqlite3 ".backup '$D/db-$(date +%F).sqlite3'"
tar czf $D/files-$(date +%F).tar.gz -C /srv/mirame/var media private
cp /srv/mirame/app/.env $D/env-$(date +%F)
find $D -mtime +30 -delete
```

Храните копии и за пределами сервера: объектное хранилище, другой сервер или хотя бы скачивание на компьютер владельца.

Проверка восстановления (раз в квартал и перед приёмкой):

```bash
sudo systemctl stop mirame
cp /srv/backups/mirame/db-YYYY-MM-DD.sqlite3 /srv/mirame/var/db.sqlite3
tar xzf /srv/backups/mirame/files-YYYY-MM-DD.tar.gz -C /srv/mirame/var
chown -R mirame:mirame /srv/mirame/var
sudo systemctl start mirame
```

Восстановление сайта A не затрагивает сайт D.

## 6. Обновление кода

Обновление готовится один раз, проверяется для обеих тем и ставится на каждый сайт **отдельно**:

```bash
cd /srv/mirame/app
sudo -u mirame git pull
sudo -u mirame /srv/mirame/venv/bin/pip install -r requirements.txt
sudo -u mirame /srv/mirame/venv/bin/python manage.py migrate
sudo -u mirame /srv/mirame/venv/bin/python manage.py collectstatic --noinput
sudo systemctl restart mirame
```

Откат: `git checkout <предыдущая версия>` и восстановление базы из копии, сделанной перед обновлением.

## 7. После запуска

Пройдите [чек-лист запуска](launch-checklist.md): домен в настройках, Яндекс Вебмастер, Google Search Console, отправка sitemap, проверка ключевых страниц, счётчики.

## Автоопределение города (необязательно)
Задайте `GEO_PROVIDER=cloudflare` (включите в Cloudflare «Add visitor location headers»: страна приходит всегда, город — только с этой настройкой; названия на английском, поэтому у городских страниц заполнено «Город (EN)») или `GEO_PROVIDER=headers` и передавайте из nginx заголовки `X-Geo-Country` / `X-Geo-City` (например, из модуля геобазы). Из внешнего мира эти заголовки нужно сбрасывать (`proxy_set_header X-Geo-City ""` до подстановки своих), иначе посетитель сможет подставить их сам — вреда нет, но предложение будет неверным. Адрес проверки: `/geo/city/` (пустой ответ `{}` — функция ничего не предлагает).
