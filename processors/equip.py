import esper

from components.actor.equip import EquipComponent
from components.actor.equipment import EquipmentComponent
from components.item.equipped import EquippedComponent
from components.item.item import ItemComponent
from components.position import PositionComponent

class EquipProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        for ent, (eqp, equipment, pos) in self.world.get_components(EquipComponent, EquipmentComponent, PositionComponent):

            for item_ent, (item, item_pos) in self.world.get_components(ItemComponent, PositionComponent):
                if pos.x == item_pos.x and pos.y == item_pos.y:
                    equipment.equipment.append(item_ent)
                    self.world.add_component(item_ent, EquippedComponent())