import esper

from components.actor.equipment import EquipmentComponent
from components.actor.remove import RemoveComponent
from components.game.message_log import MessageLogComponent
from components.game.turn_count import TurnCountComponent
from components.name import NameComponent

class RemovableProcessor(esper.Processor):
    ' This processor is a sister-processor to Wearable. WearableProcessor contains the popup menu logic. '
    def __init__(self):
        super().__init__()
    
    def process(self):
        for ent, (eqp, rem) in self.world.get_components(EquipmentComponent, RemoveComponent):
            item = rem.item_id
            name_component = self.world.component_for_entity(item, NameComponent)            
            turn = self.world.component_for_entity(1, TurnCountComponent).turn_count

            if item in eqp.equipment:
                success = True
                eqp.equipment.remove(item)                
                name_component.name = name_component._name
                self.world.component_for_entity(1, MessageLogComponent).messages.append({'remove': (name_component.name, success, turn)})
            else:
                success = False
                self.world.remove_component(ent, RemoveComponent)
                self.world.component_for_entity(1, MessageLogComponent).messages.append({'remove': (name_component.name, success, turn)})