import os
from flask import Flask
from api.pedido import pedido_api

# Instancia de la aplicación en Flask
app = Flask(__name__)

app.config.from_object('config.default_settings.Config')
app.config.from_envvar('APPLICATION_SETTINGS', True)
app.config.from_envvar('APPLICATION_SECRETS', True)

app.register_blueprint(pedido_api, url_prefix='/pedido')

# Punto de arranque: gunicorn
def gunicorn():
    return app

if __name__ == "__main__":
    app.run(
        host="0.0.0.0", port=3090, debug=True
    )