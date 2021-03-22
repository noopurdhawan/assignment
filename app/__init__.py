# import
from flask import Flask
from flask_restful import Api

# create the Flask app and start the api
app = Flask(__name__)
api = Api(app)
from app import routes

# localhost port setting to run the app
app.run(debug=True, port=8080)
