#!/usr/bin/env python3
import argparse
import numpy as np
import matplotlib
# Використовуємо бекенд 'Agg' для роботи в середовищах без дисплею
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import sys

def koch_segment(p1, p2, depth):
    """
    Рекурсивно генерує точки для сегмента фракталу Коха
    між p1 і p2 на глибині depth.
    """
    if depth == 0:
        return [p1, p2]
    one_third = p1 + (p2 - p1) / 3
    two_third = p1 + (p2 - p1) * 2 / 3
    v = two_third - one_third
    angle = np.pi / 3
    peak = one_third + np.array([
        np.cos(angle) * v[0] - np.sin(angle) * v[1],
        np.sin(angle) * v[0] + np.cos(angle) * v[1]
    ])
    pts1 = koch_segment(p1, one_third, depth - 1)
    pts2 = koch_segment(one_third, peak,    depth - 1)
    pts3 = koch_segment(peak,    two_third, depth - 1)
    pts4 = koch_segment(two_third, p2,      depth - 1)
    return pts1[:-1] + pts2[:-1] + pts3[:-1] + pts4

def make_snowflake(depth):
    """
    Повертає xs, ys для фракталу «сніжинка Коха» на рівні depth.
    """
    p1 = np.array([0.0, 0.0])
    p2 = np.array([1.0, 0.0])
    p3 = np.array([0.5, np.sqrt(3)/2])
    side1 = koch_segment(p1, p2, depth)
    side2 = koch_segment(p2, p3, depth)
    side3 = koch_segment(p3, p1, depth)
    pts = side1[:-1] + side2[:-1] + side3
    xs, ys = zip(*pts)
    return xs, ys

def main():
    parser = argparse.ArgumentParser(
        description="Генерує «сніжинку Коха» і зберігає як PNG"
    )
    parser.add_argument('-d', '--depth',
                        type=int,
                        default=3,
                        help="Рівень рекурсії (за замовчуванням: 3)")
    parser.add_argument('-o', '--output',
                        default=None,
                        help="Шлях до вихідного файлу PNG (за замовчуванням: snowflake_d<depth>.png)")
    args = parser.parse_args()

    xs, ys = make_snowflake(args.depth)

    plt.figure(figsize=(6, 6))
    plt.plot(xs, ys, linewidth=1)
    plt.axis('equal')
    plt.axis('off')
    plt.title(f'Сніжинка Коха, depth={args.depth}')

    # Визначаємо ім'я файлу
    if args.output:
        out_path = args.output
    else:
        out_path = f"snowflake_d{args.depth}.png"
    # Створюємо директорію для файлу, якщо потрібно
    os.makedirs(os.path.dirname(out_path) or '.', exist_ok=True)

    # Зберігаємо фігуру
    try:
        plt.savefig(out_path, bbox_inches='tight', pad_inches=0.1)
        print(f"Збережено фрактал у файл: {out_path}")
    except Exception as e:
        print(f"Помилка при збереженні файлу: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

# Запустіть у терміналі, вказавши бажаний рівень рекурсії:
# python3 HW03-T2.py --depth 5