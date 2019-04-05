import esper

from components.actor.equip import EquipComponent
from components.actor.equipment import EquipmentComponent
from components.game.popup import PopupComponent
from components.item.equipped import EquippedComponent
from components.item.item import ItemComponent
from components.position import PositionComponent

class EquipProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        for ent, (eqp, equipment, pos) in self.world.get_components(EquipComponent, EquipmentComponent, PositionComponent):

            if eqp.item_id is None:
                matched_items = []

                for item_ent, (item, item_pos) in self.world.get_components(ItemComponent, PositionComponent):
                    if pos.x == item_pos.x and pos.y == item_pos.y:
                        matched_items.append(item_ent)
                
                if len(matched_items) == 0:
                    self.world.remove_component(ent, EquipComponent)

                elif len(matched_items) == 1:
                    item_id = matched_items.pop()
                    equipment.equipment.append(item_id)
                    self.world.add_component(item_id, EquippedComponent())
                
                elif len(matched_items) > 1:
                    title = 'Which item do you want to pick up?'
                    choices = [('Nevermind', 'n', {'event': {'cancel': True}})] # DEBUG
                    popup_component = PopupComponent(title=title, choices=choices)
                    self.world.add_component(1, popup_component)
                    self.world.remove_component(ent, EquipComponent)

            else:
                equipment.equipment.append(eqp.item_id)
                self.world.add_component(eqp.item_id, EquippedComponent())

            
