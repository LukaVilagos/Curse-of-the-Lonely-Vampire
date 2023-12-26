class Inventory():
    def __init__(self, items: {}, max_capacity: int):
        self.items = items
        self.max_capacity = max_capacity
        self.capacity = len(items)
        
    def add_item(self, item):
        self.items.append(item)
    
    def remove_item(self, item):
        self.items.remove(item)