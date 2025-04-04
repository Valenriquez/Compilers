class Dictionary:
    def __init__(self, *args, **kwargs):
        self._data = {}
        self.update(*args, **kwargs)
    
    def length(self):
        return len(self._data)
    
    def get_item(self, key):
        return self._data[key]
    
    def set_item(self, key, value):
        self._data[key] = value
    
    def del_item(self, key):
        del self._data[key]
    
    def contains(self, key):
        return key in self._data
    
    def iter(self):
        return iter(self._data)
    
    def __repr__(self):
        return repr(self._data)
    
    def __str__(self):
        return str(self._data)
    
    def get(self, key, default=None):
        return self._data.get(key, default)
    
    def keys(self):
        return list(self._data.keys())  
    
    def values(self):
        return list(self._data.values())
    
    def items(self):
        return list(self._data.items())
    
    def update(self, *args, **kwargs):
        if args:
            if len(args) > 1:
                raise TypeError("Wrong")
            other = args[0]
            if hasattr(other, 'items'):
                for key, value in other.items():
                    self.set_item(key, value)
            else:
                for key, value in other:
                    self.set_item(key, value)
        for key, value in kwargs.items():
            self.set_item(key, value)
    
    def pop(self, key, default=None):
        if self.contains(key):
            value = self.get_item(key)
            self.del_item(key)
            return value
        if default is not None:
            return default
        raise KeyError(key)
    
    def popitem(self):
        if not self._data:
            raise KeyError("..... empty")
        key = next(iter(self._data))
        value = self.get_item(key)
        self.del_item(key)
        return (key, value)
    
    def clear(self):
        self._data.clear()
    
    def copy(self):
        return Dictionary(self._data.copy())
    
    def setdefault(self, key, default=None):
        if not self.contains(key):
            self.set_item(key, default)
        return self.get_item(key)


# Test Cases
if __name__ == "__main__":
    # Create  
    d = Dictionary()
    d.set_item('a', 1)
    d.set_item('b', 2)
    print(d)  # {a: 1, b: 2}
    
    # update
    d2 = Dictionary()
    d2.update([('x', 10), ('y', 20)], z=30)
    print(d2)  # {x: 10, y: 20, z: 30}
    
    # operations
    print(d2.length())        # 3
    print(d2.contains('x'))   # True
    print(d2.get_item('y'))   # 20
    print(d2.get('z'))        # 30
    print(d2.get('w', 0))     # 0
    
    # Update 
    d2.update({'x': 100, 'w': 40})
    print(d2)  # {x: 100, y: 20, z: 30, w: 40}
    
    print(d2.keys())    # [x, y, z, w]
    print(d2.values())  # [100, 20, 30, 40]
    print(d2.items())   # [(x, 100), (y, 20), (z, 30), (w, 40)]
    
    # Pop 
    print(d2.pop('y'))      # 20
    print(d2.popitem())     # (w, 40)
    print(d2)               # {x: 100, z: 30}
    
    # Default
    print(d2.setdefault('z', 99))  # 30
    print(d2.setdefault('new', 99)) # 99
    print(d2)                      # {x: 100, z: 30, new: 99}
    
    # Clear
    d2.clear()
    print(d2)  # {}