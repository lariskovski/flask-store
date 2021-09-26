# from typing import List
from db import db


order_item = db.Table(
    'order_item',
    db.Column("order_id", db.Integer, db.ForeignKey("orders.id")),
    db.Column("item_id", db.Integer, db.ForeignKey("items.id")))


class OrderModel(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    items = db.relationship(
        'ItemModel',
        secondary=order_item,
        backref=db.backref('orders'),
        lazy='dynamic')

    # def __init__(self) -> None:
    #     pass

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def save_to_db(self, item):
        self.items.append(item)
        db.session.commit()

    def json(self):
        return {'id': self.id, "items": [item.name for item in self.items]}
