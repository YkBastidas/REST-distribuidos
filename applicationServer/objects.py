from flask_restful import Resource
import pandas as pd
import json
import os
import socket

HOST_COORDINATOR = "127.0.0.1"
PORT_COORDINATOR = 65433


class Objects(Resource):
    def get(self):
        objects = getJSONfile()
        objects = objects.to_dict(orient="records")
        return {"objects": objects}, 200


def getJSONfile():
    root = os.path.dirname(__file__)
    filename = os.path.join(root, "objectsDatabase.json")
    file = open(filename)
    json_data = json.load(file)
    return pd.DataFrame(json_data["objects"])
