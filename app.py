from flask import Flask


app =  Flask(__name__)

# POST /store data: {name :}
app.route('/store', methods=['POST'])
def create_store():
    pass

# GET /store/<name> data: {name :}
app.route('/store/<string:name>')
def get_store(name):
    pass

# GET /store
app.route('/store')
def get_stores():
    pass

# POST /store/<name>/item data: {name :}
app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    pass

# GET /store/<name>/item data: {name :}
app.route('/store/<string:name>/item')
def get_items_in_store(name):
    pass

app.run(port=5000)