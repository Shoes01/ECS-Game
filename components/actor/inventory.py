class InventoryComponent():
    def __init__(self, inventory=None):
        if inventory:
            self.inventory = inventory # Store only the IDs of the item entities.
        else:
            self.inventory = []