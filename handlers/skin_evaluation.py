from models.skin_model import model

def img_eval(body):
    # Do prediction
    prediction = model.predict(body)

    # Process the result
    result = prediction

    return result