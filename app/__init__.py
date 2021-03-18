from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)
from app import routes

app.run(debug=True, port=8080)
