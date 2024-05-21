import time
from functools import wraps

import backoff


def mybackoff(start_sleep_time=0.1, factor=2, border_sleep_time=10):
    """
    Функция для повторного выполнения функции через некоторое время, если возникла ошибка.
    Использует наивный экспоненциальный рост времени повтора (factor) до граничного времени ожидания (border_sleep_time)

    Формула:
        t = start_sleep_time * (factor ^ n), если t < border_sleep_time
        t = border_sleep_time, иначе
    :param start_sleep_time: начальное время ожидания
    :param factor: во сколько раз нужно увеличивать время ожидания на каждой итерации
    :param border_sleep_time: максимальное время ожидания
    :return: результат выполнения функции
    """

    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            n = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    sleep_time = start_sleep_time * (factor**n)
                    if sleep_time > border_sleep_time:
                        sleep_time = border_sleep_time
                    print(f"Error: {e}, retrying in {sleep_time} seconds...")
                    time.sleep(sleep_time)
                    n += 1

        return inner

    return func_wrapper


# Пример использования:
@mybackoff(start_sleep_time=0.2, factor=3, border_sleep_time=5)
def kek_func():
    print("Trying to connect...")
    # имитация ошибки
    raise Exception("Connection error")


# def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10) -> Any:
@backoff.on_exception(lambda: backoff.expo(base=2, factor=0.1), Exception, max_time=20)
def use_lib_backoff():
    print("try", time.time())
    raise Exception("Connection error")


if __name__ == "__main__":
    # Вызываем функцию для демонстрации работы декоратора
    use_lib_backoff()
