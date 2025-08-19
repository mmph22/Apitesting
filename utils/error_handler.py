# from utils.logger import get_logger

# logger = get_logger()

# def handle_error(e, context=""):
#     logger.error(f"Error in {context}: {str(e)}")

from utils.logger import get_logger

logger = get_logger()

def handle_exception(e, context=""):
    """
    Generic error handler that logs exceptions with context.

    Args:
        e (Exception): The exception object.
        context (str): Optional context for where the error occurred.
    """
    logger.error(f"❌ Error in {context}: {str(e)}", exc_info=True)

if __name__ == "__main__":
    try:
        raise ValueError("Test error")
    except Exception as e:
        handle_exception(e, context="Test block")