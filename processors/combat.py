import esper
import tcod as libtcod

from _helper_functions import calculate_attack
from components.actor.actor import ActorComponent
from components.actor.equipment import EquipmentComponent
from components.actor.stats import StatsComponent
from components.item.modifier import ModifierComponent
from components.render import RenderComponent
from processors.death import DeathProcessor
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
            skill = event.get('skill')

            for defender_ID in defender_IDs:
                if not self.world.has_component(defender_ID, ActorComponent):
                    print('ERROR: Why is the entity attaking a non-actor?')
                    continue

                damage = calculate_attack(attacker_ID, self.world)
                defender_stats = self.world.component_for_entity(defender_ID, StatsComponent)
                
                defender_stats.hp -= damage
                
                def_ren = self.world.component_for_entity(defender_ID, RenderComponent)
                self.world.messages.append({'combat': (att_ren.char, att_ren.color, def_ren.char, def_ren.color, damage, self.world.turn)})

                if not skill:
                    self.world.get_processor(EnergyProcessor).queue.put({'ent': attacker_ID, 'bump_attack': True})

                if defender_stats.hp <= 0:
                    self.world.get_processor(DeathProcessor).queue.put({'ent': defender_ID})