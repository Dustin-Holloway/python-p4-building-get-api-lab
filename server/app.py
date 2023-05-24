#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from sqlalchemy import func

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route("/")
def index():
    return "<h1>Bakery GET API</h1>"


@app.route("/bakeries")
def bakeries():
    bakeries = []
    for bakery in Bakery.query.all():
        bakery_dict = {
            "id": bakery.id,
            "name": bakery.name,
            "created_at": bakery.created_at,
            "baked_goods": [],
        }
        for baked_good in bakery.baked_goods:
            baked_good_dict = {
                "bakery_id": baked_good.bakery_id,
                "id": baked_good.id,
                "name": baked_good.name,
                "price": baked_good.price,
                "created_at": baked_good.created_at,
                "updated_at": baked_good.updated_at,
            }
            bakery_dict["baked_goods"].append(baked_good_dict)

        bakeries.append(bakery_dict)

    response = make_response(
        jsonify(bakeries), 200, {"Content-Type": "application/json"}
    )

    return response


@app.route("/bakeries/<int:id>")
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()
    if bakery:
        bakery_dict = {
            "id": bakery.id,
            "name": bakery.name,
            "created_at": bakery.created_at,
            "baked_goods": [],
        }

        for baked_good in bakery.baked_goods:
            baked_good_dict = {
                "bakery_id": baked_good.bakery_id,
                "id": baked_good.id,
                "name": baked_good.name,
                "price": baked_good.price,
                "created_at": baked_good.created_at,
                "updated_at": baked_good.updated_at,
            }

            bakery_dict["baked_goods"].append(baked_good_dict)

        response = make_response(
            jsonify(bakery_dict), 200, {"Content-Type": "application/json"}
        )
    else:
        response = make_response(
            jsonify({"error": "Bakery not found"}),
            404,
            {"Content-Type": "application/json"},
        )

    return response


@app.route("/baked_goods/<string:by_price>")
def baked_goods_by_price(by_price):
    baked_goods = BakedGood.query.filter(BakedGood.price == by_price).all()
    baked_goods_list = []

    for baked_good in baked_goods:
        bakery = Bakery.query.get(baked_good.bakery_id)

        baked_good_dict = {
            "id": baked_good.id,
            "price": baked_good.price,
            "name": baked_good.name,
            "created_at": baked_good.created_at,
            "updated_at": baked_good.updated_at,
            "bakery": {
                "id": bakery.id,
                "name": bakery.name,
                "created_at": bakery.created_at,
                "updated_at": bakery.updated_at,
            },
        }
        baked_goods_list.append(baked_good_dict)

    response = make_response(
        jsonify(baked_goods_list), 200, {"Content-type": "application/json"}
    )

    return response


@app.route("/baked_goods/most_expensive")
def most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    bakery = Bakery.query.filter(Bakery.id == baked_good.bakery_id).first()
    bakery_dict = bakery.to_dict()

    if baked_good:
        baked_good_dict = {
            "bakery_id": baked_good.bakery_id,
            "id": baked_good.id,
            "price": baked_good.price,
            "name": baked_good.name,
            "created_at": baked_good.created_at,
            "updated_at": baked_good.updated_at,
            "bakery": bakery_dict,
        }

        response = make_response(
            jsonify(baked_good_dict), 200, {"Content-type": "application/json"}
        )
    else:
        response = make_response(
            jsonify({"error": "Bakery not found"}),
            404,
            {"Content-Type": "application/json"},
        )

    return response


if __name__ == "__main__":
    app.run(port=5555, debug=True)
