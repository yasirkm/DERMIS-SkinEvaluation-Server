import connexion

app = connexion.FlaskApp(__name__, specification_dir='api/')
app.add_api('openapi.yaml')
app.run(port=8080)