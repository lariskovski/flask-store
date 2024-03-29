from typing import List
from db import db
from models.item import ItemModel
from models.user import UserModel


order_item = db.Table(
    'order_item',
    db.Column("order_id", db.Integer, db.ForeignKey("orders.id")),
    db.Column("item_id", db.Integer, db.ForeignKey("items.id")))


class OrderModel(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    # Many to Many
    items = db.relationship(
        'ItemModel',
        secondary=order_item,
        backref=db.backref('orders'),
        lazy='dynamic')
    price = db.Column(db.Float)

    # One to Many
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('UserModel')

    def __init__(self, user_id: UserModel.id, items: List[ItemModel], price: ItemModel.price) -> None:
        self.user_id = user_id
        self.items = items
        self.price = price

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'items': [item.name for item in self.items],
            'price': self.price
        }
