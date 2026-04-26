import logging

def configureLogger(name, level=logging.INFO, log_file=None):
    """
    Configures a logger with the specified name, level, and optional log file.

    Args:
        name (str): The name of the logger.
        level (int): The logging level (e.g., logging.INFO, logging.DEBUG).
        log_file (str, optional): The path to the log file. If None, logs to console.

    Returns:
        logging.Logger: The configured logger.
    """

    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter('%(message)s')

    if log_file:
        handler = logging.FileHandler(log_file)
    else:
        handler = logging.StreamHandler()

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
