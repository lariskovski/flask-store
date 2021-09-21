from flask import Flask, jsonify, request


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
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)

# GET /store/<name> data: {name :}
@app.route('/store/<string:name>')
def get_store(name):
    pass

# GET /store
@app.route('/store')
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

app.run(port=5000, debug=True)