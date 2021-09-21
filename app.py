from flask import Flask, jsonify


app = Flask(__name__)


stores = [{
            'name': 'Awesome Flask', 
            'items': 
                [{
                    'name': 'Big HP Flask', 
                    'price': 100
                }]
            }]


# POST /store data: {name :}
@app.route('/store', methods=['POST'])
def create_store():
    pass

# GET /store/<name> data: {name :}
@app.route('/store/<string:name>')
def get_store(name):
    pass

# GET /store
@app.route('/')
def get_stores():
    return jsonify({
                    'stores': stores
                   })

# POST /store/<name>/item data: {name :}
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    pass

# GET /store/<name>/item data: {name :}
@app.route('/store/<string:name>/item')
def get_items_in_store(name):
    pass

app.run(port=5000)