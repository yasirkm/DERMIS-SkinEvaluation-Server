import base64
from io import BytesIO

import numpy as np
from PIL import Image

from tensorflow import keras

from ml_models.skin_model import model, CONDITIONS, RESOLUTION

def img_eval(body):
    # Process body of base64-encoded image to np array
    skin_image = base64.b64decode(body)
    skin_image = BytesIO(skin_image)
    skin_image = Image.open(skin_image)
    skin_image = skin_image.resize(RESOLUTION)

    skin_image = keras.preprocessing.image.img_to_array(skin_image)
    skin_image = np.expand_dims(skin_image, axis=0)
    # Do prediction
    prediction = model.predict(skin_image)
    prediction = prediction.astype('float64')
    prediction_idx = np.argmax(prediction)
    condition = CONDITIONS[prediction_idx]
    confidence = prediction[0][prediction_idx]

    # Process the result
    result = {
        'condition' : condition,
        'confidence' : confidence,
    }

    print(result)

    return result