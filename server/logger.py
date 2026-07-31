import logging

def setup_logger(name="MedicalAgent"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)


    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s] - [%(name)s] - [%(levelname)s] - [%(message)s]')
    ch.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(ch)

    return logger


logger = setup_logger()

logger.info("RAG process Started")
logger.debug("Debugging RAG process")
logger.error("RAG process Failed")
logger.critical("RAG process Critical Error")
