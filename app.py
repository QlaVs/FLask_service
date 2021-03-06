from flask import Flask, Response, request
from collections import OrderedDict
from bson import ObjectId
import pymongo
import json

app = Flask(__name__)

try:
    mongo = pymongo.MongoClient(host="localhost", port=27017)

    db = mongo["microservice"]

    mongo.server_info()

    db.create_collection("goods")

    vexpr = {
        "$jsonSchema":
        {
            "bsonType": "object",
            "required": ["Name", "Description"],
            "properties": {
                "Name": {
                    "bsonType": "string"
                },
                "Description": {
                    "bsonType": "string"
                },
                "Params": {
                    "bsonType": "object"
                }
            }
        }
    }

    cmd = OrderedDict([("collMod", "goods"),
                       ("validator", vexpr),
                       ("validationLevel", "moderate")])

    db.command(cmd)

except Exception as ex:
    print(ex)


@app.route('/create', methods=["POST"])
def create_goods():
    try:
        good = request.json
        db_response = db.goods.insert_one(good)
        return Response(response=json.dumps({"Message": "Good's created",
                                             "Good_id": f"{db_response.inserted_id}"}),
                        status=200,
                        mimetype="application/json")
    except Exception as ex:
        print(ex)
        return Response(response="Error while creating item, check fields ('Name' and 'Description' requeired)",
                        status=500)


@app.route('/get_by_id', methods=["GET"])
def good_by_id():
    try:
        data = db.goods.find_one({"_id": ObjectId(f"{request.args.get('good_id')}")})
        data["_id"] = str(data["_id"])
        return Response(response=json.dumps(data),
                        status=200,
                        mimetype="application/json")
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"Err": "No goods with such id"}))


@app.route('/get_info', methods=["GET"])
def get():
    try:
        args = list(request.args.items())
        data = {}

        for arg in args:
            if arg[0] != "Name" and arg[0] != "Description":
                data[f"Params.{arg[0]}"] = f"{arg[1]}"
            else:
                data[f"{arg[0]}"] = f"{arg[1]}"
        print(data)
        good = list(db.goods.find(data))
        if not good:
            return Response(response=json.dumps({"Err": "No goods with such params"}))
        for item in good:
            item["_id"] = str(item["_id"])
        data.clear()
        return Response(response=json.dumps(good),
                        status=200,
                        mimetype="application/json")
    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    app.run()
