import os
import json
from pathlib import Path

from tensorflow import keras
from google.cloud import storage

import dermis_utils


BASE_DIR = Path(__file__).parent
MODEL_FOLDER = os.environ['MODEL']
MODEL_FILE = 'model.h5'
CONFIG_FILE = 'model.conf'
BUCKET_NAME = os.environ['BUCKET']
BUCKET_SUBDIR = Path('ml_models')
LOCAL_SUBDIR = BASE_DIR
KEY_PATH = None if os.environ.get('ENVIRONMENT') == 'DEPLOYMENT' else BASE_DIR / 'auth' / 'service.json'

def download_folder(bucket_name, folder_path, save_path, key_path=None):
    if key_path:
        client = storage.Client.from_service_account_json(key_path)
    else:
        client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=folder_path.as_posix())

    for blob in blobs:
        if not blob.name.endswith('/'):
            blob.download_to_filename(save_path/Path(blob.name).name)

model_folder = BUCKET_SUBDIR / MODEL_FOLDER
save_folder = LOCAL_SUBDIR / MODEL_FOLDER
save_folder.mkdir(exist_ok=True)

download_folder(BUCKET_NAME, model_folder, save_folder, KEY_PATH)


# download_blob(KEY_PATH, BUCKET, MODEL_PATH_CLOUD, MODEL_PATH_LOCAL)
with open(save_folder/CONFIG_FILE) as config_file:
    config = json.load(config_file)

RESOLUTION = tuple(config['resolution'])
CONDITIONS = config['conditions']

model = keras.models.load_model(save_folder / 'model.h5')
