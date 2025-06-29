#!/usr/bin/env python3
import argparse
import os
import shutil
import sys
import logging

def parse_args():
    parser = argparse.ArgumentParser(
        description="Рекурсивно копіює файли з вихідної директорії в директорію призначення, "
                    "сортуючи їх за розширеннями в піддиректорії.")
    parser.add_argument('src', nargs='?', default='.',
                        help="Шлях до вихідної директорії (за замовчуванням: поточна теґа)")
    parser.add_argument('dst', nargs='?', default='dist',
                        help="Шлях до директорії призначення (за замовчуванням: ./dist)")
    return parser.parse_args()

def copy_and_sort(src_dir: str, dst_dir: str):
    """
    Рекурсивно проходить по src_dir, і для кожного файлу створює
    в dst_dir піддиректорію за розширенням і копіює файл туди.
    Пропускає .git, директорію призначення та їх вміст.
    """
    try:
        entries = os.listdir(src_dir)
    except (OSError, PermissionError) as e:
        logging.warning(f"Не вдалося прочитати директорію {src_dir}: {e}")
        return

    for name in entries:
        src_path = os.path.join(src_dir, name)
        # Пропускаємо папку .git цілком
        if name == '.git':
            logging.debug(f"Пропускаю .git: {src_path}")
            continue

        # Якщо це директорія — заходимо всередину, окрім випадку, коли це dst_dir
        if os.path.isdir(src_path):
            abs_src = os.path.abspath(src_path)
            abs_dst = os.path.abspath(dst_dir)
            # Якщо ця директорія є або всередині директорії призначення — пропускаємо
            if os.path.commonpath([abs_src, abs_dst]) == abs_dst:
                logging.debug(f"Пропускаю директорію призначення {abs_src}")
                continue
            copy_and_sort(abs_src, dst_dir)

        # Якщо це файл — копіюємо
        elif os.path.isfile(src_path):
            ext = os.path.splitext(name)[1].lstrip('.').lower() or 'no_ext'
            target_dir = os.path.join(dst_dir, ext)
            try:
                os.makedirs(target_dir, exist_ok=True)
            except (OSError, PermissionError) as e:
                logging.error(f"Не вдалося створити директорію {target_dir}: {e}")
                continue

            dst_path = os.path.join(target_dir, name)
            # Уникаємо копіювання, якщо шлях однаковий
            if os.path.abspath(src_path) == os.path.abspath(dst_path):
                logging.debug(f"Пропускаю копіювання самого себе: {src_path}")
                continue

            try:
                shutil.copy2(src_path, dst_path)
                logging.info(f"Скопійовано {src_path} -> {dst_path}")
            except (OSError, PermissionError, shutil.Error) as e:
                logging.error(f"Не вдалося скопіювати {src_path} -> {dst_path}: {e}")

def main():
    args = parse_args()
    src = os.path.abspath(args.src)
    dst = os.path.abspath(args.dst)

    if not os.path.isdir(src):
        logging.error(f"Вихідна директорія не знайдена: {src}")
        sys.exit(1)
    try:
        os.makedirs(dst, exist_ok=True)
    except (OSError, PermissionError) as e:
        logging.error(f"Не вдалося створити директорію призначення {dst}: {e}")
        sys.exit(1)

    logging.basicConfig(
        level=logging.INFO,
        format='[%(levelname)s] %(message)s'
    )

    logging.info(f"Починаю копіювання з {src} до {dst}")
    copy_and_sort(src, dst)
    logging.info("Завершено.")

if __name__ == "__main__":
    main()
