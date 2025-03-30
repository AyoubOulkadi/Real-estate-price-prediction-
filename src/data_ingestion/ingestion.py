import boto3
import os
import logging

from config.utils import IngestionHelper

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up S3 client
s3 = boto3.client('s3',
                  aws_access_key_id=IngestionHelper.AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=IngestionHelper.AWS_SECRET_ACCESS_KEY)


def transfer_files_S3(bucket_name, folder_path, target_folder):
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            file_key = f"{target_folder}/{filename}"
            try:
                s3.upload_file(file_path, bucket_name, file_key)
                logging.info(f"Uploaded {file_path} to S3 bucket {bucket_name} as {file_key}")
            except Exception as e:
                logging.error(f"An error occurred during uploading file to S3: {str(e)}")
                raise Exception(f"An error occurred during uploading file to S3: {str(e)}")


if __name__ == "__main__":
    transfer_files_S3(IngestionHelper.bucket_name, IngestionHelper.folder_path, IngestionHelper.target_folder)
