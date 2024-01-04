import datetime
import json
import os
script_directory = os.path.dirname(os.path.realpath(__file__))
json_file_name = "directed-radius-409718-d0d03a8a1400.json"
os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"
] =  os.path.join(script_directory, json_file_name)
from google.cloud import storage

CILENT = storage.Client()
FILE_DIR = {"audio": "temp_audios"}


class StoreGcp:
    def __init__(self, source_file_name, file_type) -> None:
        self.client = CILENT
        self.source_file_name = source_file_name
        self.file_type = file_type
        self._get_bucket_names()

    def _get_bucket_names(self) -> None:
        script_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_directory, "destination.json")

        with open(file_path, "r") as dest:
            destination = json.load(dest)
        self.bucket_name = destination[self.file_type]
        self.project_name = destination["gcp_project_name"]

    def upload_data(self):
        bucket = self.client.get_bucket(self.bucket_name)
        source_file_path = os.path.join(FILE_DIR[self.file_type], self.source_file_name)
        blob = bucket.blob(self.source_file_name)
        blob.upload_from_filename(source_file_path)

    def get_signed_url(self):
        bucket = self.client.get_bucket(self.bucket_name)
        blob = bucket.blob(self.source_file_name)
        expiration_time = datetime.timedelta(minutes=15)
        signed_url = blob.generate_signed_url(
            expiration=expiration_time, method="GET", version="v4"
        )
        return signed_url
