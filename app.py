from bson import ObjectId
from flask import Flask, Response, request
import pymongo
import json

app = Flask(__name__)

try:
    mongo = pymongo.MongoClient(host="localhost", port=27017)

    db = mongo.microservice
    mongo.server_info()

except:
    print("Err - No Connection")


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
        return Response(response=str(ex),
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
        goods = []

        for arg in args:
            if arg[0] != "Name":
                data = list(db.goods.find({f"Params.{arg[0]}": f"{arg[1]}"}))
            else:
                data = list(db.goods.find({f"{arg[0]}": f"{arg[1]}"}))
            data[0]["_id"] = str(data[0]["_id"])
            goods.append(data[0])
            data.clear()
        return Response(response=json.dumps(goods),
                        status=200,
                        mimetype="application/json")
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"Err": "No goods with such params"}))


if __name__ == '__main__':
    app.run()
