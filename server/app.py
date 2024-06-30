# #!/usr/bin/env python3
# from models import db, Restaurant, RestaurantPizza, Pizza
# from flask_migrate import Migrate
# from flask import Flask, request, make_response, jsonify
# from flask_restful import Api, Resource
# import os

# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.json.compact = False

# migrate = Migrate(app, db)

# db.init_app(app)

# api = Api(app)


# @app.route("/")
# def index():
#     return "<h1>Code challenge</h1>"

# class Restaurants(Resource):
#     def get(self):
#         restaurants = [n.to_dict() for n in Restaurant.query.all()]
#         for hero in restaurants:
#             hero.pop('restaurant_pizzas', None)
#         return make_response(restaurants, 200)

# api.add_resource(Restaurants, "/restaurants")

# class RestaurantByID(Resource):
#     def get(self, id):
#         restaurant = Restaurant.query.filter_by(id=id).first()
#         if restaurant is None:
#             return {"error": "Restaurant not found"}, 404
#         response_dict = restaurant.to_dict()
#         return response_dict, 200
    
#     def delete(self, id):
#         restaurant = Restaurant.query.filter_by(id=id).first()
#         if restaurant is None:
#             return {"error": "Restaurant not found"}, 404

#         db.session.delete(restaurant)
#         db.session.commit()
#         return {}, 204

# api.add_resource(RestaurantByID, "/restaurants/<int:id>")

# class Pizzas(Resource):
#     def get(self):
#         response_dict_list = [n.to_dict() for n in Pizza.query.all()]

#         response = make_response(
#             response_dict_list,
#             200,
#         )

#         return response
    
# api.add_resource(Pizzas, "/pizzas")

# class RestaurantPizzas(Resource):
#     def post(self):
#         try:
#             data = request.get_json()
#             price = int(data.get('price'))
#             if price < 1 or price > 30:
#                 return make_response({"errors": ["Price must be between 1 and 30"]}, 400)

#             restaurant_pizza = RestaurantPizza(
#                 pizza_id=data.get('pizza_id'),
#                 restaurant_id=data.get('restaurant_id'),
#                 price=price,
#             )
#             db.session.add(restaurant_pizza)
#             db.session.commit()
#             response_dict = restaurant_pizza.to_dict(include_restaurant=True)
#             return make_response(response_dict, 201)
#         except ValueError as e:
#             return make_response({"errors": [str(e)]}, 400)
#         except Exception as e:
#             return make_response({"errors": ["An unexpected error occurred"]}, 400)


# if __name__ == "__main__":
#     app.run(port=5555, debug=True)




#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"


@app.route('/restaurants')
def restaurants():
    restaurants = []
    for restaurant in Restaurant.query.all():
        restaurant_dict = {
            "id" : restaurant.id,
            "name": restaurant.name,
            "address": restaurant.address,
        }
        restaurants.append(restaurant_dict)
    response = make_response(restaurants, 200)
    return response


@app.route('/restaurants/<int:id>', methods = ['GET', 'DELETE'])
def restaurants_by_id(id):
    restaurant = Restaurant.query.filter_by(id=id).first()
    if request.method == 'GET': 
        if restaurant:
            restaurant_dict = restaurant.to_dict()
            response = make_response(restaurant_dict, 200)
            return response

        else:
            body = {"error": "Restaurant not found"}
            status = 404
            return (body, status)
        
    elif request.method == 'DELETE':
        if restaurant:
             db.session.delete(restaurant)
             db.session.commit()
             body = {"Deleted": True, "msg":"Restaurant deleted"}
             response = make_response(body, 204)
             return response
        else:
            body = {"error": "Restaurant not found"}
            status = 404
            return (body, status)
        

@app.route('/pizzas')
def pizzas():
    pizzas = []
    for pizza in Pizza.query.all():
        pizza_dict = {
            "id": pizza.id,
            "ingredients": pizza.ingredients,
            "name": pizza.name
        }
        pizzas.append(pizza_dict)
    response = make_response(pizzas, 200)
    return response



@app.route('/restaurant_pizzas', methods = ['GET', 'POST'])
def restaurant_pizzas():
    if request.method == 'GET':
        restaurant_pizzas = []
        for restaurant_pizza in RestaurantPizza.query.all():
            restaurant_pizza_dict = restaurant_pizza.to_dict()
            restaurant_pizzas.append(restaurant_pizza_dict)
        response = make_response(restaurant_pizzas, 200)
        return response
    
    elif request.method == 'POST':
        json_data = request.get_json()
        try:
            new_restaurant_pizza = RestaurantPizza(
                price = json_data.get("price"),
                restaurant_id = json_data.get("restaurant_id"),
                pizza_id = json_data.get("pizza_id")
            )
        except ValueError as exc:
            response_body = {"errors": ["validation errors"]}
            status = 400
            return (response_body, status)

        db.session.add(new_restaurant_pizza)
        db.session.commit()

        restaurant_pizza_dict = new_restaurant_pizza.to_dict()
        response = make_response(restaurant_pizza_dict, 201)
        return response


if __name__ == "__main__":
    app.run(port=5555, debug=True)