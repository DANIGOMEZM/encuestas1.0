from flask import Flask, render_template
from datetime import timedelta

app = Flask(__name__, static_url_path = "/static", static_folder = "static")
app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY='dev',
)
app.permanent_session_lifetime=timedelta(minutes=30)

from src.routes import userRoute
from src.routes import encuestaRoute 
from src.routes import seccionRoute
from src.routes import tipoPreguntaRoute
from src.routes import preguntaRoute
from src.routes import opcionRoute
from src.routes import preguntaRespuestaRoute
def create_app():
    app.run(debug=True, port=5000)
