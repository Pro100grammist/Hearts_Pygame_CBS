from random import randint


def calculate_result():

    x, y = randint(0, 99), randint(0, 99)

    result = (
        "game over" if x == 0 and y == 0 else
        x + y if x < y else
        0 if x == y else
        x - y if x > y else
        None
    )

    return result


if __name__ == "__main__":
    result = calculate_result()
    print(result)
