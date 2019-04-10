import esper

from components.actor.equipment import EquipmentComponent
from components.actor.inventory import InventoryComponent
from components.actor.wear import WearComponent
from components.item.wearable import WearableComponent
from components.game.message_log import MessageLogComponent
from components.game.popup import PopupComponent
from components.game.turn_count import TurnCountComponent
from components.name import NameComponent

class WearableProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        for ent, (eqp, wear) in self.world.get_components(EquipmentComponent, WearComponent):

            if wear.item_id is None:
                # Create popup menu for player to choose from.
                title = 'Which item would you like to wear or remove?'
                choices = []
                # Present the player with a list of items from their inventory that they may consume.
                n = 97
                for item in self.world.component_for_entity(ent, InventoryComponent).inventory:
                    if not self.world.has_component(item, WearableComponent):
                        continue
                    choices.append(self.generate_choice(chr(n), eqp, item))
                    n += 1
                
                choices.append(('Nevermind', 'ESC', {'event': {'cancel': True}}))
                self.world.component_for_entity(1, PopupComponent).menus.append( (title, choices) )
                self.world.remove_component(ent, WearComponent)

            else:
                # Wear the item.
                item = self.world.component_for_entity(ent, WearComponent).item_id
                if item in eqp.equipment:
                    self.world.component_for_entity(1, MessageLogComponent).messages.append({'wear_already': (self.world.component_for_entity(item, NameComponent).name, self.world.component_for_entity(1, TurnCountComponent).turn_count)})
                    eqp.equipment.remove(item)
                elif self.world.has_component(item, WearableComponent):
                    self.world.component_for_entity(1, MessageLogComponent).messages.append({'wear': (self.world.component_for_entity(item, NameComponent).name, self.world.component_for_entity(1, TurnCountComponent).turn_count)})
                    eqp.equipment.append(item)
                else:
                    self.world.component_for_entity(1, MessageLogComponent).messages.append({'wear_fail': (self.world.component_for_entity(item, NameComponent).name, self.world.component_for_entity(1, TurnCountComponent).turn_count)})
                    self.world.remove_component(ent, WearComponent)
    
    def generate_choice(self, char, eqp, item):
        name = self.world.component_for_entity(item, NameComponent).name
        if item in eqp.equipment:
            name += ' (worn)'
        result = {'action': {'wear': item}}
        return (name, char, result)