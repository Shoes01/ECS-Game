import esper

from components.actor.equipment import EquipmentComponent
from components.actor.pickup import PickupComponent
from components.game.popup import PopupComponent
from components.item.equipped import EquippedComponent
from components.item.item import ItemComponent
from components.name import NameComponent
from components.position import PositionComponent

class PickupProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        for ent, (eqpmnt, pick, pos) in self.world.get_components(EquipmentComponent, PickupComponent, PositionComponent):

            if pick.item_id is None:
                matched_items = []

                for item_ent, (item, item_pos) in self.world.get_components(ItemComponent, PositionComponent):
                    if pos.x == item_pos.x and pos.y == item_pos.y:
                        matched_items.append(item_ent)
                
                if len(matched_items) == 0:
                    self.world.remove_component(ent, PickupComponent)

                elif len(matched_items) == 1:
                    item_id = matched_items.pop()
                    eqpmnt.equipment.append(item_id)
                    self.world.add_component(item_id, EquippedComponent())
                    item_pos = self.world.component_for_entity(item_id, PositionComponent)
                    item_pos.x, item_pos.y = -1, -1
                
                elif len(matched_items) > 1:
                    title = 'Which item do you want to pick up?'
                    choices = []
                    
                    n = 97 # chr(97) is a
                    for item in matched_items:
                        name = self.world.component_for_entity(item, NameComponent).name
                        char = chr(n)
                        result = {'action': {'pick_up': item}}
                        choices.append((name, char, result))
                        n += 1

                    choices.append(('Nevermind', 'ESC', {'event': {'cancel': True}}))
                    popup_component = PopupComponent(title=title, choices=choices)
                    self.world.add_component(1, popup_component)
                    self.world.remove_component(ent, PickupComponent)

            else:
                eqpmnt.equipment.append(pick.item_id)
                self.world.add_component(pick.item_id, EquippedComponent())
                item_pos = self.world.component_for_entity(pick.item_id, PositionComponent)
                item_pos.x, item_pos.y = -1, -1

            
