import esper

from components.actor.consume import ConsumeComponent
from components.actor.inventory import InventoryComponent
from components.actor.stats import StatsComponent
from components.game.popup import PopupComponent
from components.game.message_log import MessageLogComponent
from components.game.turn_count import TurnCountComponent
from components.item.consumable import ConsumableComponent
from components.name import NameComponent

class ConsumableProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        for ent, (con) in self.world.get_component(ConsumeComponent):
            
            if con.item_id is None:
                # Create popup menu for player to choose from.
                title = 'Which item would you like to consume?'
                choices = []
                # Present the player with a list of items from their inventory that they may consume.
                n = 97
                for item in self.world.component_for_entity(ent, InventoryComponent).inventory:
                    if not self.world.has_component(item, ConsumableComponent):
                        continue
                    name = self.world.component_for_entity(item, NameComponent).name
                    char = chr(n)
                    result = {'action': {'consume': item}}
                    choices.append((name, char, result))
                    n += 1
                
                choices.append(('Nevermind', 'ESC', {'event': {'cancel': True}}))
                popup_component = self.world.component_for_entity(1, PopupComponent).menus.append( (title, choices) )
                self.world.add_component(1, popup_component)
                self.world.remove_component(ent, ConsumeComponent)

            else:
                # Consume the item.
                item = self.world.component_for_entity(ent, ConsumeComponent).item_id
                if self.world.has_component(item, ConsumableComponent):
                    self.consume_item(ent, item)
                    self.world.component_for_entity(ent, InventoryComponent).inventory.remove(item)
                    self.world.delete_entity(item)
                else:
                    self.world.component_for_entity(1, MessageLogComponent).messages.append({'consume_fail': (self.world.component_for_entity(item, NameComponent).name, self.world.component_for_entity(1, TurnCountComponent).turn_count)})
                    self.world.remove_component(ent, ConsumeComponent)

    def consume_item(self, ent, item):
        con_component = self.world.component_for_entity(item, ConsumableComponent)
        message_log_component = self.world.component_for_entity(1, MessageLogComponent)
        stas_component = self.world.component_for_entity(ent, StatsComponent)
        turn = self.world.component_for_entity(1, TurnCountComponent).turn_count

        message_log_component.messages.append({'consume_generic': (self.world.component_for_entity(item, NameComponent).name, turn)})

        for key, value in con_component.effects.items():
            if key == 'heal':
                stas_component.hp += value
                if stas_component.hp > stas_component.hp_max:
                    stas_component.hp = stas_component.hp_max
                message_log_component.messages.append({'heal': (value, turn)})
            
            elif key == 'max_hp':
                stas_component.hp_max += value
                message_log_component.messages.append({'max_hp': (value, turn)})