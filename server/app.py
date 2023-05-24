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
        }
        bakeries.append(bakery_dict)

    response = make_response(
        jsonify(bakeries), 200, {"Content-Type": "application/json"}
    )

    return response


@app.route("/bakeries/<int:id>")
def bakery_by_id(id):
    for b in Bakery.query.filter(Bakery.id == id):
        bakery_dict = {
            "id": b.id,
            "name": b.name,
            "created_at": b.created_at,
        }

    response = make_response(bakery_dict, 200, {"Content-type": "application/json"})

    return response


@app.route("/baked_goods/<string:by_price>")
def baked_goods_by_price(by_price):
    baked_goods = BakedGood.query.filter(BakedGood.price == by_price).all()
    baked_goods_list = []

    for b in baked_goods:
        baked_good_dict = {
            "id": b.id,
            "price": b.price,
            "name": b.id,
            "created_at": b.created_at,
        }
        baked_goods_list.append(baked_good_dict)
    response = make_response(
        jsonify(baked_goods_list), 200, {"Content-type": "application/json"}
    )

    return response


@app.route("/baked_goods/most_expensive")
def most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if baked_good:
        baked_good_dict = {
            "id": baked_good.id,
            "price": baked_good.price,
            "name": baked_good.name,
            "created_at": baked_good.created_at,
        }

    response = make_response(
        jsonify(baked_good_dict), 200, {"Content-type": "application/json"}
    )

    return response


if __name__ == "__main__":
    app.run(port=5555, debug=True)
