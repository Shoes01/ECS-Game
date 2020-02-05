import esper

from components.actor.equipment import EquipmentComponent
from components.actor.inventory import InventoryComponent
from components.item.consumable import ConsumableComponent
from components.item.wearable import WearableComponent
from components.name import NameComponent
from menu import PopupMenu, PopupChoice, PopupChoiceResult, PopupChoiceCondition
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
                submenu = PopupMenu(title=_name, include_description={'item': item})
                _result = {'ent': ent, 'item': item}
                
                # Consume
                _processor = ConsumableProcessor
                _validity = False
                if self.world.has_component(item, ConsumableComponent):
                    _validity = True
                _results = (PopupChoiceResult(result=_result, processor=_processor),)
                _conditions = (PopupChoiceCondition(valid=_validity), )
                submenu.contents.append(PopupChoice(name='Consume', key='c', results=_results, conditions=_conditions))

                # Drop
                _processor = DropProcessor
                _validity = True
                if item in eqp.equipment:
                    _processor = RemovableProcessor
                    _validity = False
                _results = (PopupChoiceResult(result=_result, processor=_processor),)
                _conditions = (PopupChoiceCondition(valid=_validity), )
                submenu.contents.append(PopupChoice(name='Drop', key='d', results=_results, conditions=_conditions))

                # Remove
                _processor = RemovableProcessor
                _validity = False
                if item in eqp.equipment:
                    _validity = True
                _results = (PopupChoiceResult(result=_result, processor=_processor),)
                _conditions = (PopupChoiceCondition(valid=_validity), )
                submenu.contents.append(PopupChoice(name='Remove', key='r', results=_results, conditions=_conditions))

                # Wear
                _processor = WearableProcessor
                _validity = False
                if self.world.has_component(item, WearableComponent) and item not in eqp.equipment:
                    _validity = True
                _results = (PopupChoiceResult(result=_result, processor=_processor),)
                _conditions = (PopupChoiceCondition(valid=_validity), )
                submenu.contents.append(PopupChoice(name='Wear', key='w', results=_results, conditions=_conditions))
                
                _menu_result = {'popup': submenu}
                _results = (PopupChoiceResult(result=_menu_result, processor=StateProcessor),)
                menu.contents.append(PopupChoice(name=_name, key=_key, results=_results))
                n += 1
            
            self.world.get_processor(StateProcessor).queue.put({'popup': menu})