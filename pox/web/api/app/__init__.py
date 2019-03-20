# coding=utf-8
from .routes import *
from flask import Flask
from flask_restplus import Api


# Configuração de bootstrap da aplicação
app = Flask("project")
app.config["SECRET_KEY"] = "random"

api = Api(app, title="API POX",
          description="REST interface with network information based on pox controller")

# Importação de rotas
