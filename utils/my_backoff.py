import time
from functools import wraps

from utils.logger import logger


def backoff(
    start_sleep_time: float = 0.1,
    factor: int = 2,
    border_sleep_time: int = 10,
    exceptions=(Exception,),
    attempts: int = 5,
):
    """
    Формула:
        t = start_sleep_time * (factor ^ n), если t < border_sleep_time
        t = border_sleep_time, иначе
    :param attempts: сколько попыток делать
    :param start_sleep_time: начальное время ожидания
    :param factor: во сколько раз нужно увеличивать время ожидания на каждой итерации
    :param border_sleep_time: максимальное время ожидания
    :param exceptions: список типов исключений, при которых нужно повторять вызов
    """

    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            n = 0
            while n < attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    logger.warning(f"Try to execute: {func}")
                    sleep_time = start_sleep_time * (factor**n)
                    if sleep_time > border_sleep_time:
                        sleep_time = border_sleep_time
                    time.sleep(sleep_time)
                    n += 1

        return inner

    return func_wrapper
