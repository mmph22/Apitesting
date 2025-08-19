import logging
import os
from datetime import datetime

def get_logger(name="api_logger"):
    # Create logs folder once
    os.makedirs("logs", exist_ok=True)

    # Use a global variable to keep track of the log file for this run
    # This avoids creating new files if called multiple times
    if not hasattr(get_logger, "log_file"):
        get_logger.log_file = f"logs/run_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"

    # Only configure logging once per Python session
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler(get_logger.log_file, encoding="utf-8"),
                logging.StreamHandler()
            ]
        )

    return logging.getLogger(name)
