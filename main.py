# import sys
# import os

# sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# from utils.config_loader import load_config
# from utils.api_client import fetch_api_data
# from utils.data_formatter import format_data
# from utils.storage_handler import save_local
# from utils.gcs_handler import upload_to_gcs
# from utils.error_handler import handle_error
# from utils.logger import get_logger
# from utils.config_loader import load_config



# logger = get_logger()

# def main():
#     env = os.getenv("ENV", "dev")
#     config = load_config(env)

#     defaults = config["defaults"]
#     endpoints = config["endpoints"]

#     for ep in endpoints:
#         try:
#             logger.info(f"📡 Fetching {ep['name']} from {ep['url']} ...")
#             data = fetch_api_data(ep["url"], method=ep.get("method", "GET"))

#             for fmt in ep["output_formats"]:
#                 formatted = format_data(data, fmt)
#                 local_file = save_local(formatted, fmt, ep["name"], base_path=ep.get("local_path", "output"))

#                 if not defaults["local_only"]:
#                     destination = f"{defaults['gcs_path_prefix']}/{ep['gcs_path']}/{os.path.basename(local_file)}"
#                     upload_to_gcs(
#                         defaults["bucket"],
#                         local_file,
#                         destination,
#                         create_bucket=defaults.get("create_bucket_if_missing", False)
#                     )
#         except Exception as e:
#             handle_error(e, context=ep["name"])

# if __name__ == "__main__":
#     main()
################TESTED# main.py
# import argparse
# from flask import Request
# from utils.config_loader import load_config
# from utils.logger import get_logger
# from utils.api_client import fetch_api_data
# from utils.data_formatter import save_data_formats
# from utils.storage_handler import save_local_file
# from utils.gcs_handler import upload_to_gcs
# from utils.error_handler import handle_exception

# logger = get_logger()


# def run_pipeline(env: str = "dev") -> None:
#     """
#     Run the full ETL pipeline for a given environment.

#     Steps:
#         1. Load environment-specific config.
#         2. Fetch API data for each endpoint.
#         3. Save data to local formats (csv/json/txt).
#         4. Upload to GCS if enabled.
#     """
#     try:
#         config = load_config(env)
#         logger.info(f"🔧 Running pipeline in environment: {env}")

#         for endpoint in config.get("endpoints", []):
#             logger.info(f"📡 Fetching data for endpoint: {endpoint['name']}")

#             # Step 1: Fetch data
#             data = fetch_api_data(endpoint["url"], endpoint.get("method", "GET"))

#             # Step 2: Save in multiple formats
#             file_paths = save_data_formats(endpoint, data)

#             # Step 3: Save locally
#             for file_path in file_paths:
#                 save_local_file(file_path)

#                 # Step 4: Upload to GCS if not local_only
#                 if not config["defaults"]["local_only"]:
#                     upload_to_gcs(
#                         bucket_name=config["defaults"]["bucket"],
#                         source_file=file_path,
#                         destination_blob=f"{config['defaults']['gcs_path_prefix']}/"
#                                          f"{endpoint['gcs_path']}/"
#                                          f"{file_path.split('/')[-1]}",
#                         create_bucket=config["defaults"]["create_bucket_if_missing"],
#                     )

#         logger.info("✅ Pipeline execution completed successfully")

#     except Exception as e:
#         handle_exception(e)
#         raise


# # -------------------------------
# # Entry point for Google Cloud Function
# # -------------------------------
# def main(request: Request):
#     """
#     HTTP Cloud Function entry point.
#     Example:
#         curl "https://REGION-PROJECT_ID.cloudfunctions.net/api-pipeline?env=qa"
#     """
#     env = request.args.get("env", "dev")  # default is "dev"
#     run_pipeline(env)
#     return f"Pipeline executed for environment: {env}", 200


# # -------------------------------
# # Entry point for local execution
# # -------------------------------
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Run API pipeline locally.")
#     parser.add_argument("--env", default="dev", help="Environment: dev | qa | prod")
#     args = parser.parse_args()

#     run_pipeline(args.env)
##########################################TESTEDEND#######################
# main.py
import argparse
import os
from flask import Request
from utils.config_loader import load_config
from utils.logger import get_logger
from utils.api_client import fetch_api_data
from utils.data_formatter import save_data_formats
from utils.storage_handler import save_local_file
from utils.gcs_handler import upload_to_gcs
from utils.error_handler import handle_exception

logger = get_logger()


def run_pipeline(env: str = "dev") -> None:
    """
    Run the full ETL pipeline for a given environment.

    Args:
        env (str): Environment to run the pipeline in (dev, qa, prod).

    Workflow:
        1. Load environment-specific configuration from YAML.
        2. Fetch data from all configured API endpoints.
        3. Save API response in multiple formats (csv/json/txt).
        4. Store locally (output/ for local runs, /tmp/ for GCF).
        5. Upload to Google Cloud Storage if enabled in config.
    """
    try:
        # Step 1: Load config
        config = load_config(env)
        logger.info(f"🔧 Running pipeline in environment: {env}")

        # Step 2: Process each API endpoint
        for endpoint in config.get("endpoints", []):
            logger.info(f"📡 Fetching data for endpoint: {endpoint['name']}")

            # Fetch data
            data = fetch_api_data(endpoint["url"], endpoint.get("method", "GET"))

            # Save in configured formats
            file_paths = save_data_formats(endpoint, data)

            # Save locally (uses /tmp in GCF, output/ locally)
            for file_path in file_paths:
                save_local_file(file_path)

                # Upload to GCS if not local_only
                if not config["defaults"]["local_only"]:
                    destination_blob = (
                        f"{config['defaults']['gcs_path_prefix']}/"
                        f"{endpoint['gcs_path']}/"
                        f"{os.path.basename(file_path)}"
                    )
                    upload_to_gcs(
                        bucket_name=config["defaults"]["bucket"],
                        source_file=file_path,
                        destination_blob=destination_blob,
                        create_bucket=config["defaults"]["create_bucket_if_missing"],
                    )

        logger.info("✅ Pipeline execution completed successfully")

    except Exception as e:
        handle_exception(e)
        raise


def main(request: Request):
    """
    Google Cloud Function HTTP entry point.

    Args:
        request (flask.Request): Incoming HTTP request object.

    Returns:
        tuple: Response message and HTTP status code.

    Example:
        curl "https://REGION-PROJECT_ID.cloudfunctions.net/api-pipeline?env=qa"
    """
    env = request.args.get("env", "dev")  # Default to 'dev'
    run_pipeline(env)
    return f"Pipeline executed for environment: {env}", 200


if __name__ == "__main__":
    """
    Local execution entry point.
    Example:
        python main.py --env qa
    """
    parser = argparse.ArgumentParser(description="Run API pipeline locally.")
    parser.add_argument("--env", default="dev", help="Environment: dev | qa | prod")
    args = parser.parse_args()

    run_pipeline(args.env)

