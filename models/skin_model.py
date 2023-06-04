import os
from pathlib import Path

from tensorflow import keras
from google.cloud import storage


BASE_DIR = Path(__file__).parent
MODEL_FILE = 'model.h5'
MODEL_PATH_LOCAL = BASE_DIR/ 'files' / MODEL_FILE
MODEL_PATH_CLOUD = os.environ['MODEL_PATH_CLOUD']
BUCKET = os.environ('BUCKET')
KEY_PATH = BASE_DIR / 'auth' / 'service.json'


def download_blob(key_path, bucket, object_path, save_path):
    client = storage.Client.from_service_account_json(key_path)
    bucket = client.get_bucket(bucket)
    blob = bucket.blob(object_path)
    blob.download_to_filename(save_path)


download_blob(KEY_PATH, BUCKET, MODEL_PATH_CLOUD, MODEL_PATH_LOCAL)
model = keras.models.load_model(MODEL_PATH_LOCAL)