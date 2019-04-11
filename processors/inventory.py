import esper

from components.actor.equipment import EquipmentComponent
from components.actor.inventory import InventoryComponent
from components.actor.open_inv import OpenInventoryComponent
from components.game.popup import PopupComponent, PopupMenu, PopupChoice
from components.item.consumable import ConsumableComponent
from components.item.wearable import WearableComponent
from components.name import NameComponent

class InventoryProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        for ent, (eqp, inv, op_inv) in self.world.get_components(EquipmentComponent, InventoryComponent, OpenInventoryComponent):
            # Generate a list of items that the player may select.
            # Selecting an item opens a submenu with possible actions.
            menu = PopupMenu(title='Inventory')
            
            n = 97
            for item in inv.inventory:
                _name = self.world.component_for_entity(item, NameComponent).name
                if item in eqp.equipment:
                    _name += ' (worn)'
                _key = chr(n)
                
                # Prepare the result of the menu: the submenu!
                submenu = PopupMenu(title=_name)
                
                # Consume
                _result = {'consume': item}
                _validity = False
                if self.world.has_component(item, ConsumableComponent):
                    _validity = True
                submenu.contents.append(PopupChoice(name=_name, key=_key, result=_result, valid=_validity))

                # Drop
                _result = {'drop': item}
                _validity = True
                if item in eqp.equipment:
                    _result = {'wear': item} # If the player tries to drop the item, they will unequip it instead.
                    _validity = False
                submenu.contents.append(PopupChoice(name=_name, key=_key, result=_result, valid=_validity))

                # Remove
                _result = {'wear': item}
                _validity = False
                if item in eqp.equipment:
                    _validity = True
                submenu.contents.append(PopupChoice(name=_name, key=_key, result=_result, valid=_validity))

                # Wear
                _result = {'wear': item}
                _validity = False
                if self.world.has_component(item, WearableComponent):
                    _validity = True
                submenu.contents.append(PopupChoice(name=_name, key=_key, result=_result, valid=_validity))
                
                _menu_result = {'popup': submenu}
                menu.contents.append(PopupChoice(name=_name, key=_key, result=_menu_result, action=False))
                n += 1
            
            self.world.component_for_entity(1, PopupComponent).menus.append(menu)
            self.world.remove_component(ent, OpenInventoryComponent)