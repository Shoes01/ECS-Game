import esper

from components.actor.open_inv import OpenInventoryComponent
from components.actor.inventory import InventoryComponent
from components.game.popup import PopupComponent
from components.name import NameComponent

class InventoryProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        for ent, (inv, op_inv) in self.world.get_components(InventoryComponent, OpenInventoryComponent):

            # Create popup menu for player to choose from.
            title = 'Inventory'
            choices = []
            # Present the player with a list of items from their inventory that they may consume.
            n = 97
            for item in inv.inventory:
                name = self.world.component_for_entity(item, NameComponent).name
                char = chr(n)
                result = {'action': {'DEBUG': True}}
                choices.append((name, char, result))
                n += 1
            
            choices.append(('Nevermind', 'ESC', {'event': {'cancel': True}}))
            popup_component = PopupComponent(title=title, choices=choices)
            self.world.add_component(1, popup_component)
            self.world.remove_component(ent, OpenInventoryComponent)