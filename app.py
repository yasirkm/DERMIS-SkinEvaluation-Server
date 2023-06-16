import connexion

from PIL import UnidentifiedImageError

from handlers.error import invalid_image_encoding

options = {'swagger_url': '/'}

app = connexion.FlaskApp(__name__, specification_dir='api/', options=options)
app.add_api('openapi.yaml')
app.add_error_handler(UnidentifiedImageError, invalid_image_encoding)

app.run(port=8080)