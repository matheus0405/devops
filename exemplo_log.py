import logging

LOGGER = logging.getLogger("devops")
LOGGER.setLevel(logging.DEBUG)

formatter = logging.Formatter(fmt="%(name)s | %(levelname)s | %(asctime)s | %(filename)s:%(lineno)s | %(message)s")

file_handler = logging.FileHandler("devops.log", encoding="utf-8")
file_handler.setFormatter(formatter)

handler = logging.StreamHandler()
handler.setFormatter(formatter)

LOGGER.addHandler(file_handler)
LOGGER.addHandler(handler)

LOGGER.info("Teste!")
LOGGER.debug("DEBUG!")