#!/usr/bin/env python3
"""Загрузчик фотографий в рубрики сайта через API импорта (раздел 11.2 ТЗ).

Работает на обычном Python 3.9+ без дополнительных пакетов.

Настройка — файл профиля (пример: tools/uploader.example.ini):

    [mirame]
    url = https://mirame.ru
    token_file = ~/.config/art-uploader/mirame.token   ; ключ хранится отдельно, не в репозитории
    [mirame.folders]
    ~/Картины/Море = 12
    ~/Картины/Абстракция = 7

Команды:
    python uploader.py --config uploader.ini --profile mirame --categories   # показать рубрики и их ID
    python uploader.py --config uploader.ini --profile mirame                # загрузить (с подтверждением)
    python uploader.py --config uploader.ini --profile mirame --dry-run      # только показать план

Повторный запуск безопасен: уже принятые файлы сервер узнает по external_id
и не создает дубликатов, поэтому незавершенную загрузку достаточно запустить снова.
"""
import argparse
import configparser
import hashlib
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def load_profile(config_path, name):
    cfg = configparser.ConfigParser(inline_comment_prefixes=(";", "#"))
    cfg.optionxform = str  # сохранять регистр путей
    if not cfg.read(config_path, encoding="utf-8"):
        sys.exit(f"Не найден файл настроек: {config_path}")
    if name not in cfg:
        sys.exit(f"В {config_path} нет профиля [{name}]. Есть: {', '.join(cfg.sections())}")
    section = cfg[name]
    url = section.get("url", "").rstrip("/")
    if not url.startswith("https://") and not url.startswith("http://localhost") and not url.startswith("http://127.0.0.1"):
        sys.exit("Адрес сайта должен начинаться с https://")
    token = os.environ.get(section.get("token_env", "ART_IMPORT_TOKEN"), "")
    if not token and section.get("token_file"):
        token_path = Path(section["token_file"]).expanduser()
        if token_path.exists():
            token = token_path.read_text(encoding="utf-8").strip()
    if not token:
        sys.exit("Не найден ключ API: укажите token_file в профиле или переменную окружения ART_IMPORT_TOKEN.")
    folders = {}
    folder_section = f"{name}.folders"
    if folder_section in cfg:
        for folder, cat_id in cfg[folder_section].items():
            folders[Path(folder).expanduser()] = int(cat_id)
    return {"name": name, "url": url, "token": token, "folders": folders, "purpose": section.get("purpose", "photo")}


def request(profile, method, path, fields=None, file_path=None, retries=4):
    url = profile["url"] + path
    headers = {"Authorization": f"Bearer {profile['token']}", "Accept": "application/json"}
    body = None
    if fields is not None:
        boundary = uuid.uuid4().hex
        parts = []
        for key, value in fields.items():
            parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{key}"\r\n\r\n{value}\r\n'.encode())
        if file_path:
            mime = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
            safe_name = urllib.parse.quote(file_path.name)
            parts.append(
                f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="{safe_name}"\r\n'
                f"Content-Type: {mime}\r\n\r\n".encode() + file_path.read_bytes() + b"\r\n"
            )
        parts.append(f"--{boundary}--\r\n".encode())
        body = b"".join(parts)
        headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
    delay = 2
    for attempt in range(retries + 1):
        req = urllib.request.Request(url, data=body, method=method, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                return resp.status, json.loads(resp.read().decode() or "{}")
        except urllib.error.HTTPError as exc:
            try:
                payload = json.loads(exc.read().decode() or "{}")
            except ValueError:
                payload = {"message": exc.reason}
            if exc.code == 429 and attempt < retries:
                time.sleep(60)
                continue
            return exc.code, payload
        except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:
            if attempt == retries:
                return 0, {"message": f"Нет связи с сайтом: {exc}"}
            time.sleep(delay)
            delay *= 2
    return 0, {"message": "Нет связи с сайтом"}


def external_id(profile, folder, file_path):
    rel = file_path.relative_to(folder).as_posix()
    digest = hashlib.sha1(f"{folder.name}/{rel}".encode()).hexdigest()[:10]
    return f"{profile['name']}:{folder.name}/{rel}"[:180] + f"#{digest}"


def show_categories(profile):
    status, data = request(profile, "GET", "/api/v1/import/categories")
    if status != 200:
        sys.exit(f"Ошибка {status}: {data.get('message')}")
    print(f"Рубрики сайта {profile['url']}:")
    for cat in data["categories"]:
        print(f"  ID {cat['id']:>4}  {cat['path']}{'' if cat['visible'] else '  (скрыта)'}")


def plan(profile):
    items = []
    for folder, cat_id in profile["folders"].items():
        if not folder.is_dir():
            print(f"! Папка не найдена: {folder}")
            continue
        for path in sorted(folder.rglob("*")):
            if path.is_file() and path.suffix.lower() in EXTENSIONS:
                items.append((folder, cat_id, path))
    return items


def main():
    parser = argparse.ArgumentParser(description="Загрузка фотографий в рубрики сайта через API импорта")
    parser.add_argument("--config", default="uploader.ini")
    parser.add_argument("--profile", required=True, help="Имя профиля — конкретный сайт")
    parser.add_argument("--categories", action="store_true", help="Показать рубрики и их ID")
    parser.add_argument("--dry-run", action="store_true", help="Только показать план загрузки")
    parser.add_argument("--yes", action="store_true", help="Не спрашивать подтверждение")
    args = parser.parse_args()

    profile = load_profile(args.config, args.profile)
    if args.categories:
        show_categories(profile)
        return
    status, data = request(profile, "GET", "/api/v1/import/categories")
    if status != 200:
        sys.exit(f"Ключ не принят сайтом ({status}): {data.get('message')}")
    categories = {c["id"]: c["path"] for c in data["categories"]}

    items = plan(profile)
    print(f"Сайт: {profile['url']}  (профиль «{profile['name']}»)")
    for folder, cat_id in profile["folders"].items():
        target = categories.get(cat_id, "!! рубрика не найдена на сайте")
        count = sum(1 for f, _, _ in items if f == folder)
        print(f"  {folder}  →  ID {cat_id} «{target}»  — файлов: {count}")
    missing = [cid for cid in profile["folders"].values() if cid not in categories]
    if missing:
        sys.exit("Исправьте ID рубрик в настройках: " + ", ".join(map(str, missing)))
    if args.dry_run or not items:
        return
    if not args.yes and input("Загрузить? [да/нет] ").strip().lower() not in {"да", "д", "yes", "y"}:
        return

    ok = dup = failed = 0
    for folder, cat_id, path in items:
        ext_id = external_id(profile, folder, path)
        status, data = request(profile, "POST", "/api/v1/import/images",
                               fields={"external_id": ext_id, "category_id": cat_id, "purpose": profile["purpose"]},
                               file_path=path)
        if status == 0:
            # Связь оборвалась: проверяем, успел ли сервер принять файл.
            status, data = request(profile, "GET", "/api/v1/import/results/" + urllib.parse.quote(ext_id, safe=""))
        if status in (200, 201) and data.get("ok"):
            if data.get("duplicate"):
                dup += 1
                print(f"= уже загружен: {path.name}")
            else:
                ok += 1
                print(f"+ принят: {path.name} → {data.get('state_display')}")
        else:
            failed += 1
            print(f"! {path.name}: {status} {data.get('message', '')}")
    print(f"\nГотово. Принято: {ok}, уже были: {dup}, ошибок: {failed}.")
    if failed:
        print("Файлы с ошибками можно исправить и запустить загрузку снова — принятые не задвоятся.")


if __name__ == "__main__":
    main()
