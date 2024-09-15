import logging

__all__ = ["logger"]

# create logger
logger = logging.getLogger("PyCardano Chain Context")  # type: ignore

# create console handler and set level to debug
ch = logging.StreamHandler()  # type: ignore

# create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")  # type: ignore

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)
