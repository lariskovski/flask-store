from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse, request

from models.order import OrderModel
from models.item import ItemModel
# from models.user import UserModel


class Order(Resource):

    parser = reqparse.RequestParser()

    @jwt_required()
    def get(self, _id):
        order = OrderModel.find_by_id(_id)
        if order:
            return {"user_id": order.user_id, "items": [item.name for item in order.items]}
        return {'message': 'order not found'}, 404

    @jwt_required()
    def post(self):

        data = request.json

        user_id = get_jwt_identity()

        items = []

        items_names = data['items']
        for item in items_names:
            try:
                item_object = ItemModel.find_by_name(item)
                items.append(item_object)
            except Exception as e:
                print(e)
                return {"message": "An error occurred inserting the order"}, 500

        order = OrderModel(items, user_id)
        order.save_to_db()
        return {"id": order.id, "user_id": order.user_id, "items": [item.name for item in order.items]}, 201


class OrderList(Resource):

    def get(self):
        return {"orders": [order.json() for order in OrderModel.get_all()]}
