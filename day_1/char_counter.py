import numpy as np
from collections import Counter


def chars_probabilities_counter(inp_str: str) -> dict:
    """
    приймає рядок і повертає словник у якому: ключами є всі символи,
    які зустрічаються в цьому рядку,а значеннями - відповідні вірогідності
    зустріти цей символ в цьому рядку.
    """
    try:
        total = len(inp_str)  # визначаємо загальну кількість символів
        counted_chars = Counter(inp_str)  # рахуємо кількість повторень
        chars, counts = zip(*counted_chars.items())
        probabilities = np.array(counts) / total * 100  # рахуємо вірогідність

        return dict(zip(chars, probabilities))

    except ValueError:
        print("Поле вводу не повинно бути порожнім!")
        repeat = input('Якщо бажаєте повторити введіть Y: ')
        if repeat == 'Y':
            inp_string = input('Введіть рядок: ')
            print(chars_probabilities_counter(inp_string))


if __name__ == "__main__":
    input_string = input('Введіть рядок: ')
    print(chars_probabilities_counter(input_string))
