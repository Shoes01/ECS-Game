import esper

from components.actor.equipment import EquipmentComponent
from components.name import NameComponent
from processors.energy import EnergyProcessor
from queue import Queue

class RemovableProcessor(esper.Processor):
    ' This processor is a sister-processor to Wearable. WearableProcessor contains the popup menu logic. '
    def __init__(self):
        super().__init__()
        self.queue = Queue()
    
    def process(self):
        while not self.queue.empty():
            event = self.queue.get()

            ent = event['ent']
            item = event['item']

            eqp = self.world.component_for_entity(ent, EquipmentComponent)
            name_component = self.world.component_for_entity(item, NameComponent)            
            turn = self.world.turn

            if item in eqp.equipment:
                success = True
                eqp.equipment.remove(item)                
                name_component.name = name_component._name
                self.world.messages.append({'remove': (name_component.name, success, turn)})
                self.world.get_processor(EnergyProcessor).queue.put({'ent': ent, 'remove': True})
            else:
                success = False
                self.world.messages.append({'remove': (name_component.name, success, turn)})