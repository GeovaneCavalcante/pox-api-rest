# coding=utf-8
from flask import Flask
from flask_restplus import Api
from flask_cors import CORS

# Configuração de bootstrap da aplicação
app = Flask("project")
app.config["SECRET_KEY"] = "random"

CORS(app)

api = Api(app, title="API POX",
          description="REST interface with network information based on pox controller")

# Importação de rotas
from .routes import *
