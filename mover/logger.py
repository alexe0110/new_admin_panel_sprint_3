import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
my_handler = logging.StreamHandler()
my_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s \t %(message)s")
my_handler.setFormatter(my_formatter)

logger.addHandler(my_handler)
