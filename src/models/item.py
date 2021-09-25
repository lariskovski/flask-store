import sqlite3

class ItemModel:

    def __init__(self, name, price) -> None:
        self.name = name
        self.price = price


    def json(self):
        return {'name': self.name, 'price': self.price}


    @classmethod
    def insert(cls, item):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        insert_query = "INSERT INTO items VALUES (?,?)"
        cursor.execute(insert_query, (item['name'], item['price']))
        conn.commit()
        conn.close()


    @classmethod
    def find_by_name(cls, name):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        
        query = "SELECT * FROM items WHERE name=?"

        result = cursor.execute(query, (name,))
        row = result.fetchone()

        conn.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}, 200
        return None
