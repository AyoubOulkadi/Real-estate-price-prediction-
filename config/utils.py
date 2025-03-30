class IngestionHelper:
    AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
    AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
    bucket_name = 'sarouty-bucket'
    folder_path = '/Data/raw_Data/'
    target_folder = "raw_data"

