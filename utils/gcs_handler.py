from google.cloud import storage
from google.cloud.exceptions import NotFound, GoogleCloudError
from utils.logger import get_logger
import os

logger = get_logger()

def get_or_create_bucket(client, bucket_name, create_if_missing=False):
    """
    Retrieves a GCS bucket. Creates it if it doesn't exist and create_if_missing is True.

    Args:
        client (google.cloud.storage.Client): GCS client instance.
        bucket_name (str): Name of the bucket.
        create_if_missing (bool): Whether to create the bucket if it doesn't exist.

    Returns:
        google.cloud.storage.Bucket: The bucket object.

    Raises:
        FileNotFoundError: If bucket doesn't exist and create_if_missing is False.
        GoogleCloudError: If bucket creation fails.
    """
    try:
        bucket = client.get_bucket(bucket_name)
        logger.info(f"✅ Found bucket: {bucket_name}")
    except NotFound:
        if create_if_missing:
            try:
                bucket = client.create_bucket(bucket_name)
                logger.info(f"🪣 Created bucket: {bucket_name}")
            except GoogleCloudError as e:
                logger.error(f"❌ Failed to create bucket '{bucket_name}': {e}")
                raise
        else:
            raise FileNotFoundError(f"Bucket '{bucket_name}' does not exist.")
    return bucket

def upload_file_to_bucket(bucket, source_file, destination_blob):
    """
    Uploads a local file to a GCS bucket if it doesn't already exist.

    Args:
        bucket (google.cloud.storage.Bucket): Target GCS bucket.
        source_file (str): Path to the local file.
        destination_blob (str): Destination path in the bucket.

    Returns:
        None
    """
    blob = bucket.blob(destination_blob)
    if blob.exists(bucket.client):  # Correct way to check existence
        logger.info(f"⚠️ File already exists in GCS: {destination_blob}")
    else:
        try:
            blob.upload_from_filename(source_file)
            logger.info(f"☁️ Uploaded to GCS: gs://{bucket.name}/{destination_blob}")
        except Exception as e:
            logger.error(f"❌ Failed to upload file '{source_file}' to GCS: {e}")
            raise

def upload_to_gcs(bucket_name, source_file, destination_blob, create_bucket=False):
    """
    High-level function to upload a file to GCS, with optional bucket creation.

    Args:
        bucket_name (str): Name of the GCS bucket.
        source_file (str): Path to the local file.
        destination_blob (str): Destination path in the bucket.
        create_bucket (bool): Whether to create the bucket if it doesn't exist.

    Returns:
        None
    """
    try:
        client = storage.Client()
        bucket = get_or_create_bucket(client, bucket_name, create_if_missing=create_bucket)
        upload_file_to_bucket(bucket, source_file, destination_blob)
    except Exception as e:
        logger.error(f"🚨 Upload to GCS failed: {e}")
        raise