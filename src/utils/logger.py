import logging
import os

def setup_logging():
    """
    Set up logging for the application.
    """
    os.makedirs("logs", exist_ok=True)

    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # Set the base logger level

    # Create handlers
    app_handler = logging.FileHandler("logs/app.log", encoding="utf-8")
    error_handler = logging.FileHandler("logs/error.log", encoding="utf-8")
    console_handler = logging.StreamHandler()

    # Set levels for each handler
    app_handler.setLevel(logging.INFO)  # Logs everything from INFO level and above
    error_handler.setLevel(logging.ERROR)  # Logs only ERROR and CRITICAL level logs
    console_handler.setLevel(logging.INFO)  # Logs INFO and above to the console

    # Define the log format
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    app_handler.setFormatter(formatter)
    error_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(app_handler)
    logger.addHandler(error_handler)
    logger.addHandler(console_handler)
