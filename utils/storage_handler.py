# import os
# from datetime import datetime
# from utils.logger import get_logger

# logger = get_logger()

# def save_local(data, fmt, endpoint_name, base_path="output"):
#     folder = os.path.join(base_path, fmt, endpoint_name)
#     os.makedirs(folder, exist_ok=True)
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     file_path = os.path.join(folder, f"{endpoint_name}_{timestamp}.{fmt}")

#     with open(file_path, "w", encoding="utf-8") as f:
#         f.write(data)

#     logger.info(f"💾 Saved locally: {file_path}")
#     return file_path
##############################################################################TESTEDCODE##############################
# import os
# from datetime import datetime
# from utils.logger import get_logger

# logger = get_logger()

# def save_local_file(content: str, file_extension: str = "txt", file_name: str = None, folder: str = "output") -> str:
#     """
#     Save content to a local file with a timestamped name.

#     Args:
#         content (str): The data to write to the file.
#         file_extension (str): File format/extension (e.g., 'json', 'csv', 'txt').
#         file_name (str): Optional base name for the file. Defaults to 'data'.
#         folder (str): Directory to save the file in.

#     Returns:
#         str: Full path to the saved file.
#     """
#     os.makedirs(folder, exist_ok=True)
#     timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
#     base_name = file_name or "data"
#     full_name = f"{base_name}_{timestamp}.{file_extension}"
#     file_path = os.path.join(folder, full_name)

#     with open(file_path, "w", encoding="utf-8") as f:
#         f.write(content)

#     logger.info(f"💾 Saved file: {file_path}")

#     return file_path
    ########################################### END##########################################

import os
from datetime import datetime
from utils.logger import get_logger

logger = get_logger()


def is_running_in_gcf() -> bool:
    """
    Detect if the code is running inside Google Cloud Functions.

    Returns:
        bool: True if running inside GCF, False otherwise.
    """
    return "K_SERVICE" in os.environ or "FUNCTION_NAME" in os.environ


def save_local_file(
    content: str,
    file_extension: str = "txt",
    file_name: str = None,
    folder: str = "output"
) -> str:
    """
    Save content to a local file with a timestamped name.
    Works in both local and Google Cloud Function environments.

    Args:
        content (str): The data to write to the file.
        file_extension (str): File format/extension (e.g., 'json', 'csv', 'txt').
        file_name (str): Optional base name for the file. Defaults to 'data'.
        folder (str): Directory to save the file in (ignored in GCF).

    Returns:
        str: Full path to the saved file.
    """
    # If running in GCF, always use /tmp
    if is_running_in_gcf():
        folder = "/tmp"

    # Ensure folder exists
    os.makedirs(folder, exist_ok=True)

    # Create timestamped filename
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    base_name = file_name or "data"
    full_name = f"{base_name}_{timestamp}.{file_extension}"
    file_path = os.path.join(folder, full_name)

    # Write file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    logger.info(f"💾 Saved file: {file_path}")
    return file_path
