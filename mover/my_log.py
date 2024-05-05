import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
my_handler = logging.StreamHandler()
my_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s \t %(message)s")
my_handler.setFormatter(my_formatter)

logger.addHandler(my_handler)

if __name__ == "__main__":
    logger.info("kekek")
