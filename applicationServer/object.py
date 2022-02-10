import json
import os
from flask_restful import Resource, reqparse
from objects import getJSONfile
from datetime import datetime
import pandas as pd

root = os.path.dirname(__file__)
filename = os.path.join(root, "objectsDatabase.json")


class Object(Resource):
    def get(self, name=None):
        return self.get_object_by_name(name)

    def get_object_by_name(self, name):
        objects = getJSONfile()
        if name in list(objects["name"]):
            findName = objects["name"] == name
            objects = objects.loc[findName]
            objects = objects.to_dict(orient="records")
            return {"objects": objects}, 200
        else:
            return {"message": f"Object {name} not found"}, 409

    def post(self, name=None):
        objects = getJSONfile()
        print(objects)
        if name in list(objects["name"]):
            return {"message": f"'{name}' already exists."}, 409
        else:
            new_object = pd.DataFrame(
                {
                    "creation_date": [datetime.now().strftime("%d/%m/%Y %H:%M:%S")],
                    "name": name,
                    "action": ["Undefined"],
                }
            )
            objects = objects.append(new_object, ignore_index=True)
            objects = {"objects": objects.to_dict(orient="records")}
            with open(filename, "w") as outfile:
                json.dump(objects, outfile)
            return objects, 201

    def delete(self, name=None):

        objects = getJSONfile()

        if name in list(objects["name"]):
            objects = objects[objects["name"] != name]
            objects = {"objects": objects.to_dict(orient="records")}
            with open(filename, "w") as outfile:
                json.dump(objects, outfile)
            return objects, 204
        else:
            return {"message": f"'{name}' object not found."}, 404
