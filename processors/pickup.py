import esper

from components.actor.inventory import InventoryComponent
from components.item.item import ItemComponent
from components.name import NameComponent
from components.persist import PersistComponent
from components.position import PositionComponent
from menu import PopupMenu, PopupChoice
from processors.energy import EnergyProcessor
from processors.state import StateProcessor
from queue import Queue

class PickupProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.queue = Queue()
    
    def process(self):
        while not self.queue.empty():
            event = self.queue.get()

            ent = event['ent']
            item = event['item']

            inv = self.world.component_for_entity(ent, InventoryComponent)
            pos = self.world.component_for_entity(ent, PositionComponent)
            turn = self.world.turn

            if item is True:
                matched_items = []

                for item_ent, (item, item_pos) in self.world.get_components(ItemComponent, PositionComponent):
                    if pos.x == item_pos.x and pos.y == item_pos.y:
                        matched_items.append(item_ent)
                
                if len(matched_items) == 0:
                    self.world.messages.append({'pickup': (None, False, turn)})

                elif len(matched_items) == 1:
                    self.pick_up(ent, matched_items.pop(), inv, turn)
                
                elif len(matched_items) > 1:
                    # Create popup menu for player to choose from.
                    menu = PopupMenu(title='Which item do you want to pick up?')
                    
                    n = 97
                    for item in matched_items:
                        _name = self.world.component_for_entity(item, NameComponent).name
                        _key = chr(n)
                        _result = {'pick_up': item}
                        menu.contents.append(PopupChoice(name=_name, key=_key, result=_result))
                        n += 1

                    self.world.get_processor(StateProcessor).queue.put({'popup': menu})

            else:
                self.pick_up(ent, item, inv, turn)
    
    def pick_up(self, ent, item, inv_component, turn):
        # Attach item to player.
        inv_component.inventory.append(item)
        self.world.add_component(item, PersistComponent())

        # Remove the item from the map.
        self.world.remove_component(item, PositionComponent)

        self.world.get_processor(EnergyProcessor).queue.put({'ent': ent, 'pick_up': True})
        self.world.messages.append({'pickup': (self.world.component_for_entity(item, NameComponent).name, True, turn)})
