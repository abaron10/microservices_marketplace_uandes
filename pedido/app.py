import os
from flask import Flask

# Instancia de la aplicación en Flask
app = Flask(__name__)

app.config.from_object('config.default_settings.Config')
app.config.from_envvar('APPLICATION_SETTINGS', True)
app.config.from_envvar('APPLICATION_SECRETS', True)

#from api.sesion import sesion_api
#app.register_blueprint(sesion_api, url_prefix='/sesion')

# Punto de arranque: gunicorn
def gunicorn():
    return app

if __name__ == "__main__":
    app.run(
        host="0.0.0.0", port=3020, debug=True
    )