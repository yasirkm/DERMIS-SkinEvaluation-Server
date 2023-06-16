import connexion

options = {'swagger_url': '/'}

app = connexion.FlaskApp(__name__, specification_dir='api/', options=optinos)
app.add_api('openapi.yaml')
app.run(port=8080)