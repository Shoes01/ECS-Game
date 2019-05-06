import esper
import tcod as libtcod

from _helper_functions import calculate_power
from components.actor.actor import ActorComponent
from components.actor.dead import DeadComponent
from components.actor.equipment import EquipmentComponent
from components.actor.stats import StatsComponent
from components.item.modifier import ModifierComponent
from components.render import RenderComponent
from processors.energy import EnergyProcessor
from queue import Queue

class CombatProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.queue = Queue()
    
    def process(self):
        while not self.queue.empty():
            event = self.queue.get()

            attacker_ID = event['ent']
            att_ren = self.world.component_for_entity(attacker_ID, RenderComponent)

            defender_IDs = event['defender_IDs']

            for defender_ID in defender_IDs:

                if not self.world.has_component(defender_ID, ActorComponent):
                    return 0
                
                defender_stats = self.world.component_for_entity(defender_ID, StatsComponent)

                damage = calculate_power(attacker_ID, self.world)

                defender_stats.hp -= damage

                def_ren = self.world.component_for_entity(defender_ID, RenderComponent)

                self.world.messages.append({'combat': (att_ren.char, att_ren.color, def_ren.char, def_ren.color, damage, self.world.turn)})
                self.world.get_processor(EnergyProcessor).queue.put({'ent': attacker_ID, 'bump_attack': True})

                if defender_stats.hp <= 0 and not self.world.has_component(defender_ID, DeadComponent):
                    self.world.add_component(defender_ID, DeadComponent(murderer=attacker_ID))