import esper

from components.actor.consume import ConsumeComponent
from components.actor.inventory import InventoryComponent
from components.actor.stats import StatsComponent
from components.item.consumable import ConsumableComponent
from components.name import NameComponent
from menu import PopupMenu, PopupChoice

class ConsumableProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        for ent, (con) in self.world.get_component(ConsumeComponent):
            
            if con.item_id is None:
                # Create popup menu for player to choose from.
                menu = PopupMenu(title='Which item would you like to consume?')

                n = 97
                for item in self.world.component_for_entity(ent, InventoryComponent).inventory: 
                    if not self.world.has_component(item, ConsumableComponent):
                        continue
                    _name = self.world.component_for_entity(item, NameComponent).name
                    _key = chr(n)
                    _result = {'consume': item}
                    menu.contents.append(PopupChoice(name=_name, key=_key, result=_result))
                    n += 1
                
                self.world.popup_menus.append(menu)
                self.world.remove_component(ent, ConsumeComponent)

            else:
                # Consume the item.
                item = self.world.component_for_entity(ent, ConsumeComponent).item_id
                name = self.world.component_for_entity(item, NameComponent).name
                turn = self.world.turn

                if self.world.has_component(item, ConsumableComponent):
                    success = True
                    self.world.messages.append({'consume': (name, success, turn)})
                    self.consume_item(ent, item, turn)
                    self.world.component_for_entity(ent, InventoryComponent).inventory.remove(item)
                    self.world.delete_entity(item)
                else:
                    success = False
                    self.world.messages.append({'consume': (name, success, turn)})
                    self.world.remove_component(ent, ConsumeComponent)

    def consume_item(self, ent, item, turn):
        con_component = self.world.component_for_entity(item, ConsumableComponent)
        stas_component = self.world.component_for_entity(ent, StatsComponent)
        
        for key, value in con_component.effects.items():
            if key == 'heal':
                stas_component.hp += value
                if stas_component.hp > stas_component.hp_max:
                    stas_component.hp = stas_component.hp_max
                self.world.messages.append({'heal': (value, turn)})
            
            elif key == 'max_hp':
                stas_component.hp_max += value
                self.world.messages.append({'max_hp': (value, turn)})