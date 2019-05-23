import esper

from components.actor.equipment import EquipmentComponent
from components.actor.inventory import InventoryComponent
from components.item.consumable import ConsumableComponent
from components.item.wearable import WearableComponent
from components.name import NameComponent
from menu import PopupMenu, PopupChoice
from processors.consumable import ConsumableProcessor
from processors.drop import DropProcessor
from processors.event import EventProcessor
from processors.removable import RemovableProcessor
from processors.wearable import WearableProcessor
from processors.state import StateProcessor
from queue import Queue

class InventoryProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.queue = Queue()
    
    def process(self):
        while not self.queue.empty():
            event = self.queue.get()

            ent = event['ent']

            eqp = self.world.component_for_entity(ent, EquipmentComponent)
            inv = self.world.component_for_entity(ent, InventoryComponent)

            # Generate a list of items that the player may select.
            # Selecting an item opens a submenu with possible actions.
            menu = PopupMenu(title='Inventory', auto_close=False)
            
            n = 97
            for item in inv.inventory:
                _name = self.world.component_for_entity(item, NameComponent).name
                _key = chr(n)
                
                # Prepare the result of the menu: the submenu!
                submenu = PopupMenu(title=_name)
                _result = {'ent': ent, 'item': item}
                
                # Consume
                _processor = ConsumableProcessor
                _validity = False
                if self.world.has_component(item, ConsumableComponent):
                    _validity = True
                submenu.contents.append(PopupChoice(name='Consume', key='c', result=_result, valid=_validity, processor=_processor))

                # Drop
                _processor = DropProcessor
                _validity = True
                if item in eqp.equipment:
                    _processor = RemovableProcessor
                    _validity = False
                submenu.contents.append(PopupChoice(name='Drop', key='d', result=_result, valid=_validity, processor=DropProcessor))

                # Remove
                _processor = RemovableProcessor
                _validity = False
                if item in eqp.equipment:
                    _validity = True
                submenu.contents.append(PopupChoice(name='Remove', key='r', result=_result, valid=_validity, processor=RemovableProcessor))

                # Wear
                _processor = WearableProcessor
                _validity = False
                if self.world.has_component(item, WearableComponent) and item not in eqp.equipment:
                    _validity = True
                submenu.contents.append(PopupChoice(name='Wear', key='w', result=_result, valid=_validity, processor=_processor))
                
                _menu_result = {'popup': submenu}
                menu.contents.append(PopupChoice(name=_name, key=_key, result=_menu_result, processor=StateProcessor))
                n += 1
            
            self.world.get_processor(StateProcessor).queue.put({'popup': menu})