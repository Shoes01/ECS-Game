import esper

from components.actor.inventory import InventoryComponent
from components.item.consumable import ConsumableComponent
from components.name import NameComponent
from components.stats import StatsComponent
from menu import PopupMenu, PopupChoice
from processors.energy import EnergyProcessor
from processors.soul import SoulProcessor
from processors.state import StateProcessor
from queue import Queue

class ConsumableProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.queue = Queue()
    
    def process(self):
        while not self.queue.empty():
            event = self.queue.get()

            consumed = event.get('consumed')
            ent = event['ent']
            item = event.get('item')
            
            if consumed:
                self.world.component_for_entity(ent, InventoryComponent).inventory.remove(consumed)
                self.world.delete_entity(consumed)
                self.world.get_processor(EnergyProcessor).queue.put({'ent': ent, 'consume': True})
                continue

            if not item:
                # Create popup menu for player to choose from.
                menu = PopupMenu(title='Which item would you like to consume?')

                n = 97
                for item in self.world.component_for_entity(ent, InventoryComponent).inventory: 
                    if not self.world.has_component(item, ConsumableComponent):
                        continue
                    _name = self.world.component_for_entity(item, NameComponent).name
                    _key = chr(n)
                    _result = {'ent': ent, 'item': item}
                    menu.contents.append(PopupChoice(name=_name, key=_key, result=_result, processor=ConsumableProcessor))
                    n += 1
                
                self.world.get_processor(StateProcessor).queue.put({'popup': menu})

            else:
                # Consume the item.
                name = self.world.component_for_entity(item, NameComponent).name
                turn = self.world.turn

                if self.world.has_component(item, ConsumableComponent):
                    success = True
                    self.world.messages.append({'consume': (name, success, turn)})
                    self.consume_item(ent, item, turn)
                else:
                    success = False
                    self.world.messages.append({'consume': (name, success, turn)})

    def consume_item(self, ent, item, turn):
        con_component = self.world.component_for_entity(item, ConsumableComponent)
        stats_component = self.world.component_for_entity(ent, StatsComponent)
        
        for key, value in con_component.effects.items():
            if key == 'heal':
                stats_component.hp += value
                self.world.messages.append({'heal': (value, turn)})
                self.queue.put({'consumed': item})
            
            elif key == 'soul':
                self.world.get_processor(SoulProcessor).queue.put({'soul': value, 'jar': item})
