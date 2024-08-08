# my_logging_module.py

import logging

def setup_custom_logger(name, log_level=logging.INFO, log_file=None):
    """
    Sets up a custom logger with specified log level and optional log file.

    Args:
        name (str): Name of the logger.
        log_level (int, optional): Log level (e.g., logging.DEBUG, logging.INFO). Defaults to logging.INFO.
        log_file (str, optional): Path to the log file. If None, logs will be printed to console only.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Optionally, add a file handler
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

# Example usage:
if __name__ == "__main__":
    # Create a logger named "my_app"
    my_logger = setup_custom_logger("my_app", log_level=logging.DEBUG, log_file="my_app.log")

    # Log messages
    my_logger.debug("Debug message")
    my_logger.info("Info message")
    my_logger.warning("Warning message")
    my_logger.error("Error message")
    my_logger.critical("Critical message")
