from flask import Flask
from flask_restful import Api
from objects import Objects
from object import Object

app = Flask(__name__)
api = Api(app)
api.add_resource(Objects, "/api/objects/")
api.add_resource(Object, "/api/objects/<name>")

if __name__ == "__main__":
    app.run()
