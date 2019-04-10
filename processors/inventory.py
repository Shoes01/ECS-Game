import esper

from components.actor.equipment import EquipmentComponent
from components.actor.inventory import InventoryComponent
from components.actor.open_inv import OpenInventoryComponent
from components.game.popup import PopupComponent
from components.item.consumable import ConsumableComponent
from components.item.wearable import WearableComponent
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
        eligibility = True

        if not self.world.has_component(item, ConsumableComponent):
            eligibility = False
        action_choice = ('Consume', 'c', {'action': {'consume': item}}, eligibility)

        action_drop = ('Drop', 'd', {'action': {drop_or_wear: item}})

        eligibility = True
        if not self.world.has_component(item, WearableComponent):
            eligibility = False
        action_wear = ('Wear', 'w', {'action': {'wear': item}}, eligibility)

        action_nevermind = ('Nevermind', 'ESC', {'event': {'cancel': True}})

        choices = [action_choice, action_drop, action_wear, action_nevermind]

        return {'event': {'popup': (title, choices)}}