from flask_restful import Resource, reqparse
from objects import getJSONfile
import pandas as pd
from datetime import datetime


class Object(Resource):
    def get(self, name=None):
        return self.get_object_by_name(name)

    def get_object_by_name(self, name):
        objects = getJSONfile()
        if name in list(objects["name"]):
            findName = objects["name"] == name
            objects = objects.loc[findName]
            print(objects)
            objects = objects.to_dict()
            return {"objects": objects}, 200
            # return {"object": objects[name]}, 200
        else:
            return {"message": f"Object {name} not found"}, 409

    def post(self, name=None):
        objects = getJSONfile()
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
            objects.to_json("newObjectsDatabase.json")
            return {"objects": objects.to_dict()}, 201

    def delete(self, name=None):

        objects = getJSONfile()

        if name in list(objects["name"]):
            objects = objects[objects["name"] != name]
            objects.to_json("newObjectsDatabase.json")
            return {"objects": objects.to_dict()}, 204
        else:
            return {"message": f"'{name}' object not found."}, 404
