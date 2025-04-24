import boto3
import os
import logging
import argparse

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def parse_parameters():
    """
    Parses parameters from the command line.

    Returns
    -------
    tuple
      (bucket_name, source, selected_params)
    """

    cmd_arg_parser = argparse.ArgumentParser(allow_abbrev=False)

    cmd_arg_parser.add_argument('--bucket-name', type=str, required=True,
                                help='Bucket name to store files in S3')
    cmd_arg_parser.add_argument('--folder-path', type=str, required=True,
                                help='Actual Path within the data exists')
    cmd_arg_parser.add_argument('--target-folder', type=str, required=True,
                                help='folder to store the daily data')

    args = cmd_arg_parser.parse_args()
    return args


def get_credentials():
    AWS_ACCESS_KEY_ID = ""
    AWS_SECRET_ACCESS_KEY = ""
    return AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY


def transfer_files_S3(s3, bucket_name, folder_path, target_folder):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, folder_path)
            s3_key = os.path.join(target_folder, relative_path).replace("\\", "/")

            try:
                s3.upload_file(local_path, bucket_name, s3_key)
                logging.info(f"Uploaded {local_path} to S3 bucket {bucket_name} as {s3_key}")
            except Exception as e:
                logging.error(f"Error uploading {local_path} to S3: {str(e)}")
                raise Exception(f"Error uploading {local_path} to S3: {str(e)}")


if __name__ == "__main__":
    args = parse_parameters()
    aws_access_key, aws_secret_key = get_credentials()

    s3 = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key
    )
    transfer_files_S3(s3, args.bucket_name, args.folder_path, args.target_folder)
