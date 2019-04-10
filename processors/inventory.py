import esper

from components.actor.equipment import EquipmentComponent
from components.actor.inventory import InventoryComponent
from components.actor.open_inv import OpenInventoryComponent
from components.game.popup import PopupComponent
from components.name import NameComponent

class InventoryProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        for ent, (eqp, inv, op_inv) in self.world.get_components(EquipmentComponent, InventoryComponent, OpenInventoryComponent):

            # Create popup menu for player to choose from.
            title = 'Inventory'
            choices = []
            # Present the player with a list of items from their inventory that they may consume.
            n = 97
            for item in inv.inventory:
                name = self.world.component_for_entity(item, NameComponent).name
                drop_or_wear = 'drop'
                if item in eqp.equipment:
                    name += ' (worn)'
                    drop_or_wear = 'wear'
                char = chr(n)
                result = self.generate_results(item, name, drop_or_wear)
                choices.append((name, char, result))
                n += 1
            
            choices.append(('Nevermind', 'ESC', {'event': {'cancel': True}}))
            self.world.component_for_entity(1, PopupComponent).menus.append( (title, choices) )
            self.world.remove_component(ent, OpenInventoryComponent)
    
    def generate_results(self, item, name, drop_or_wear):
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
                {'action': {drop_or_wear: item}}
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