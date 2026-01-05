import boto3
from botocore import UNSIGNED
from botocore.config import Config
from pathlib import Path
from src.logging_configuration import logger

def download_file_from_s3(bucket_name, key_name, local_path):

    Path(f"{local_path}").parent.mkdir(parents=True, exist_ok=True)
    
    s3_client = boto3.client(
        's3',
        region_name='us-west-2',
        config=Config(signature_version=UNSIGNED)
        )

    logger.info("Starting file download")
    logger.info(f"Destination: {local_path}")
    s3_client.download_file(bucket_name, key_name, local_path)
    logger.info("File downloaded sucessfuly")