

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


if __name__ == "__main__":
    flask = Store('Flask Store')
    flask.add_item('HP Potion', 10)
    flask.add_item('MP Potion', 10)
    flask.add_item('Strength Potion', 20)
    print(flask.stock_price())

    big = Store('Big Fask Store', [{'name': 'Invulnerability Potion', 'price': 100}])
    print(big.stock_price())