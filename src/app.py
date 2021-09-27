from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask import Flask

from resources.item import Item, ItemList
from resources.user import UserRegister, User, UserLogin, UserList
from resources.order import Order, OrderList

from db import db

from gevent.pywsgi import WSGIServer
from gevent import monkey

monkey.patch_all()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'onetwothree'
db.init_app(app)

api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


# Creates /auth
# Returns access token
jwt = JWTManager(app)


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Order, '/order', '/order/<string:_id>')
api.add_resource(OrderList, '/orders')
api.add_resource(User, '/user/<string:user_id>')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserList, '/users')


if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)

    # use gevent WSGI server instead of the Flask
    http = WSGIServer(('', 5000), app.wsgi_app)

    # Serve your application
    http.serve_forever()
