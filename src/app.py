from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://SamLR18:Pass18d@cluster0.1vzbl.mongodb.net/inventorydoulos?retryWrites=true&w=majority"
mongo = PyMongo(app)

CORS(app)

db = mongo.db.products


@app.route("/products", methods=["POST"])
def createProducts():
    id = db.insert(
        {
            "product": request.json["product"],
            "price": request.json["price"],
            "quantity": request.json["quantity"],
        }
    )
    return jsonify(str(ObjectId(id)))


@app.route("/products/", methods=["GET"])
def getProducts():
    users = []
    for doc in db.find():
        users.append(
            {
                "_id": str(ObjectId(doc["_id"])),
                "product": doc["product"],
                "price": doc["price"],
                "quantity": doc["quantity"],
            }
        )
    return jsonify(users)


@app.route("/products/<id>", methods=["GET"])
def getProduct(id):
    user = db.find_one({"_id": ObjectId(id)})
    print(user)
    return jsonify(
        {
            "_id": str(ObjectId(user["_id"])),
            "product": user["product"],
            "price": user["price"],
            "quantity": user["quantity"],
        }
    )


@app.route("/products/<id>", methods=["DELETE"])
def deleteProducts(id):
    db.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Product Deleted"})


@app.route("/products/<id>", methods=["PUT"])
def updateProducts(id):
    print(request.json)
    db.update_one(
        {"_id": ObjectId(id)},
        {
            "$set": {
                "product": request.json["product"],
                "price": request.json["price"],
                "quantity": request.json["quantity"],
            }
        },
    )
    return jsonify({"message": "Product Updated"})


if __name__ == "__main__":
    app.run(debug=True)
