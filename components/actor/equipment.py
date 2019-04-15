class EquipmentComponent():
    def __init__(self, equipment=None):
        if equipment:
            self.equipment = equipment # Store only the IDs of the item entities.
        else:
            self.equipment = []