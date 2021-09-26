from flask_jwt import jwt_required
from flask_restful import Resource, reqparse, request

from models.order import OrderModel
from models.item import ItemModel


class Order(Resource):

    parser = reqparse.RequestParser()

    @jwt_required()
    def get(self, _id):
        order = OrderModel.find_by_id(_id)
        if order:
            return {"items": [item.name for item in order.items]}
        return {'message': 'order not found'}, 404

    def post(self):

        data = request.json
        print(data)

        order = OrderModel()
        items = data['items']
        for item in items:
            try:
                item_object = ItemModel.find_by_name(item)
                order.save_to_db(item_object)
            except Exception as e:
                print(e)
                return {"message": "An error occurred inserting the order"}, 500

        return {"id": order.id, "items": [item.name for item in order.items]}, 201


class OrderList(Resource):

    def get(self):
        return {"orders": [order.json() for order in OrderModel.get_all()]}
