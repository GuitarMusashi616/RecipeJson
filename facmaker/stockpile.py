from typing import Union, Dict


class Stockpile:
    """Wraps a dictionary of string:int representing item name and quantity eg. copper:5"""

    def __init__(self, stock: Union[None, Dict[str, int]] = None):
        if stock is None:
            stock = {}
        self.stock = stock

    def __repr__(self):
        return f"{self.stock}"

    def __bool__(self):
        return bool(self.stock)

    def __getitem__(self, key: str):
        return self.stock[key]

    def __setitem__(self, key: str, val: int):
        self.stock[key] = val

    def __add__(self, other: Union[Dict[str, int], "Stockpile"]):
        return self.combine(other)

    def __iadd__(self, other: Union[Dict[str, int], "Stockpile"]):
        self.merge(other)
        return self

    def __sub__(self, other):
        return self.separate(other)

    def __isub__(self, other):
        self.split(other)
        return self

    def __mul__(self, num):
        output = self.copy()
        output *= num
        return output

    def __imul__(self, num):
        self.mult(num)
        return self

    def __iter__(self):
        return iter(self.stock.items())

    def __contains__(self, key: Union[str, Dict[str, int], "Stockpile"]):
        if type(key) is str:
            return key in self.stock
        else:
            return self.contains(key)

    def contains(self, other: Union[Dict[str, int], "Stockpile"]):
        """Returns true if all contents of other are included in self"""
        for item, amount in other.items():
            if item not in self.stock or self.stock[item] < amount:
                return False
        return True

    def copy(self):
        return self.__class__(self.stock.copy())

    def items(self):
        for item, amount in self.stock.items():
            yield item, amount

    def merge(self, other: Union[Dict[str, int], "Stockpile"]):
        """Take other stockpile and add it to self"""
        for item, amount in other.items():
            self.add(item, amount)

    def split(self, other: Union[Dict[str, int], "Stockpile"]):
        """Remove contents of other from self"""
        for item, amount in other.items():
            self.stock[item] -= amount

    def combine(self, other):
        """Take 2 stockpiles and return a 3rd with contents from both"""
        output = self.__class__()
        output.merge(self)
        output.merge(other)
        return output

    def separate(self, other):
        """Take 2 stockpiles and return a 3rd with contents of 1st - contents of 2nd"""
        output = self.__class__()
        output.merge(self)
        output.split(other)
        return output

    def add(self, item: str, count: int = 1):
        if item not in self.stock:
            self.stock[item] = 0
        self.stock[item] += count

    def sub(self, item: str, count: int = 1):
        assert item in self.stock, f"cannot remove {item} from {self.stock}"
        self.stock[item] -= count

    def mult(self, multiplier):
        for item in self.stock:
            self.stock[item] *= multiplier
