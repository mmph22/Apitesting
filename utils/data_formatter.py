# import pandas as pd
# import json

# def format_data(data, fmt="json"):
#     if fmt == "json":
#         return json.dumps(data, indent=2)
#     elif fmt == "csv":
#         if isinstance(data, dict) and "variables" in data:
#             df = pd.DataFrame(data["variables"]).T.reset_index()
#             return df.to_csv(index=False)
#         elif isinstance(data, list):
#             df = pd.DataFrame(data[1:], columns=data[0])
#             return df.to_csv(index=False)
#         else:
#             df = pd.DataFrame([data])
#             return df.to_csv(index=False)
#     elif fmt == "txt":
#         return json.dumps(data, indent=2)
#     else:
#         raise ValueError(f"Unsupported format: {fmt}")

##################### Below code ###########################
# import os
# import json
# import pandas as pd
# from datetime import datetime
# from utils.logger import get_logger

# logger = get_logger()

# def format_data(data, fmt="json"):
#     if fmt == "json":
#         return json.dumps(data, indent=2)
#     elif fmt == "csv":
#         if isinstance(data, dict) and "variables" in data:
#             df = pd.DataFrame(data["variables"]).T.reset_index()
#             return df.to_csv(index=False)
#         elif isinstance(data, list):
#             df = pd.DataFrame(data[1:], columns=data[0])
#             return df.to_csv(index=False)
#         else:
#             df = pd.DataFrame([data])
#             return df.to_csv(index=False)
#     elif fmt == "txt":
#         return json.dumps(data, indent=2)
#     else:
#         raise ValueError(f"Unsupported format: {fmt}")

# def save_data_formats(endpoint: dict, data: dict) -> list:
#     formats = endpoint.get("formats", ["json"])
#     name = endpoint.get("name", "data")
#     timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
#     folder = "output"
#     os.makedirs(folder, exist_ok=True)

#     file_paths = []

#     for fmt in formats:
#         formatted_data = format_data(data, fmt)
#         file_name = f"{name}_{timestamp}.{fmt}"
#         file_path = os.path.join(folder, file_name)

#         with open(file_path, "w", encoding="utf-8") as f:
#             f.write(formatted_data)

#         logger.info(f"💾 Saved file: {file_path}")
#         file_paths.append(file_path)

#     return file_paths

################################### END OF CODE #####################################
import os
import json
import pandas as pd
from datetime import datetime
from utils.logger import get_logger

logger = get_logger()

def format_data(data, fmt="json"):
    """
    Format data into the specified format.

    Args:
        data (dict or list): Raw data to format.
        fmt (str): Format type ("json", "csv", "txt").

    Returns:
        str: Formatted string.

    Raises:
        ValueError: If format is unsupported.
    """
    if not isinstance(data, (dict, list)):
        raise TypeError("Data must be a dict or list.")

    if fmt == "json":
        return json.dumps(data, indent=2)

    elif fmt == "txt":
        # Text format - simplified version of the JSON dump, or line-based string.
        if isinstance(data, dict):
            return "\n".join(f"{k}: {v}" for k, v in data.items())
        elif isinstance(data, list):
            return "\n".join(map(str, data))
        else:
            return str(data)

    elif fmt == "csv":
        if isinstance(data, dict):
            if "variables" in data and isinstance(data["variables"], dict):
                df = pd.DataFrame(data["variables"]).T.reset_index()
            elif all(isinstance(v, (list, tuple)) for v in data.values()):
                df = pd.DataFrame.from_dict(data, orient='index').reset_index()
            else:
                df = pd.DataFrame([data])
        elif isinstance(data, list):
            try:
                # If it's a list of lists with a header
                df = pd.DataFrame(data[1:], columns=data[0])
            except Exception:
                df = pd.DataFrame(data)
        else:
            df = pd.DataFrame([data])
        return df.to_csv(index=False)

    else:
        raise ValueError(f"Unsupported format: {fmt}")


def save_data_formats(endpoint: dict, data: dict, folder: str = "output") -> list:
    """
    Save formatted data to disk in multiple formats.

    Args:
        endpoint (dict): Contains 'name' and 'formats' keys.
        data (dict or list): Raw data to save.
        folder (str): Directory where files should be saved.

    Returns:
        list: List of saved file paths.
    """
    formats = endpoint.get("formats", ["json"])
    name = endpoint.get("name", "data")
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")

    os.makedirs(folder, exist_ok=True)

    file_paths = []

    for fmt in formats:
        try:
            formatted_data = format_data(data, fmt)
            file_name = f"{name}_{timestamp}.{fmt}"
            file_path = os.path.join(folder, file_name)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(formatted_data)

            logger.info(f"💾 Saved file: {file_path}")
            file_paths.append(file_path)

        except Exception as e:
            logger.error(f"❌ Failed to save {fmt} format: {e}")

    return file_paths
