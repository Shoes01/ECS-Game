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
                result = self.generate_results(item, name)
                choices.append((name, char, result))
                n += 1
            
            choices.append(('Nevermind', 'ESC', {'event': {'cancel': True}}))
            self.world.component_for_entity(1, PopupComponent).menus.append( (title, choices) )
            self.world.remove_component(ent, OpenInventoryComponent)
    
    def generate_results(self, item, name):
        title = name
        choices = [
            (
                'Consume',
                'c',
                {'action': {'consume': item}}
            ),
            (
                'Drop',
                'd',
                {'action': {'drop': item}}
            ),
            (
                'Wear',
                'w',
                {'action': {'wear': item}}
            ),
            (
                'Nevermind',
                'ESC',
                {'event': {'cancel': True}}
            )
        ]

        return {'event': {'popup': (title, choices)}}