

class Store:
    def __init__(self, name: str, items=None):
        self.name = name
        self.items = [] if items == None else items


    def add_item(self, name: str, price: int) -> None:
        item = {"name": name, "price": price}
        self.items.append(item)


    def stock_price(self) -> int:
        # Add together all item prices in self.items and return the total.
        return sum([item['price'] for item in self.items])


    @classmethod
    def franchise(cls, store: "Store") -> "Store":
        return cls(store.name + ' - franchise')


    @staticmethod
    def store_details(store: "Store") -> str:
        return f"{store.name}, total stock price: {store.stock_price()}"

if __name__ == "__main__":

    flask = Store('Fask Store', [{'name': 'Invulnerability Potion', 'price': 100}])
    print(Store.store_details(flask))
    print(flask.stock_price())

    flask_franchise = Store.franchise(flask)
    print(flask_franchise.name)
    flask_franchise.add_item('HP Potion', 10)
    flask_franchise.add_item('MP Potion', 10)
    flask_franchise.add_item('Strength Potion', 20)
    print(flask_franchise.stock_price())