import os
import json
from pathlib import Path

from tensorflow import keras
from google.cloud import storage

import dermis_utils


BASE_DIR = Path(__file__).parent
MODEL_FOLDER = 'skinv1' #os.environ['MODEL']
MODEL_FILE = 'model.h5'
CONFIG_FILE = 'model.conf'
BUCKET_NAME = 'dts-model' #os.environ('BUCKET')
BUCKET_SUBDIR = Path('/')
LOCAL_SUBDIR = BASE_DIR
KEY_PATH = BASE_DIR / 'auth' / 'service.json'

# CONDITIONS = ["Actinic Keratosis", "Basal Cell Carcinoma", "Benign Keratosis", "Dermatofibroma", "Melanoma", "Melanocytic Nevus", "Squamous cell carcinoma", "Vascular Lesion"]
# RESOLUTION = (240,240)

def download_folder(key_path, bucket_name, folder_path, save_path):
    client = storage.Client.from_service_account_json(key_path)
    bucket = client.get_bucket(bucket_name)
    blobs = bucket.list_blobs()

    for blob in blobs:
        print(blob.name)
        blob.download_to_filename(save_path/blob.name)

model_folder = BUCKET_SUBDIR / MODEL_FOLDER
save_folder = LOCAL_SUBDIR / MODEL_FOLDER
save_folder.mkdir(exist_ok=True)

download_folder(KEY_PATH, BUCKET_NAME, model_folder, save_folder.parent)


# download_blob(KEY_PATH, BUCKET, MODEL_PATH_CLOUD, MODEL_PATH_LOCAL)
with open(save_folder/CONFIG_FILE) as config_file:
    config = json.load(config_file)

RESOLUTION = tuple(config['resolution'])
CONDITIONS = config['conditions']

model = keras.models.load_model(save_folder / 'model.h5')
