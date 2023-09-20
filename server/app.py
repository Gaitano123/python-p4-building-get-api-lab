#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from sqlalchemy import desc

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()
    bakeries_list =[]
    for bakery in bakeries:
        bakery_dict = {
            'id':bakery.id,
            'name': bakery.name,
            'created_at':bakery.created_at,
            'updated_at':bakery.updated_at
        }
        bakeries_list.append(bakery_dict)

    return make_response(jsonify(bakeries_list),200)


@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()
    bakery_dict = bakery.to_dict()
    response = make_response(
        jsonify(bakery_dict),
        200
    )
    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    goods = []
    
    for good in BakedGood.query.order_by(desc(BakedGood.price)).all():
        good_dict = {
            'id': good.id,
            'name':good.name,
            'created_at': good.created_at,
            'updated_at': good.updated_at,
            'bakery_id': good.bakery_id,
            'price': good.price
        }
        goods.append(good_dict)
        
    response = make_response(
        goods, 
        200
    )
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    expensive = BakedGood.query.order_by(desc(BakedGood.price)).first()
    
    good = expensive.to_dict()
    
    return make_response(jsonify(good), 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
