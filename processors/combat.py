import esper
import tcod as libtcod

from _helper_functions import calculate_attack, calculate_magic_attack
from components.actor.actor import ActorComponent
from components.actor.equipment import EquipmentComponent
from components.render import RenderComponent
from components.stats import StatsComponent
from components.furniture import FurnitureComponent
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
            counter_attack = event.get('counter_attack')
            skill = event.get('skill')

            for defender_ID in defender_IDs:
                if not self.world.has_component(defender_ID, ActorComponent):
                    print('ERROR: Why is the entity attaking a non-actor?')
                    continue

                damage = 0

                att_stats = self.world.component_for_entity(attacker_ID, StatsComponent)
                def_stats = self.world.component_for_entity(defender_ID, StatsComponent)

                double_attack = att_stats.speed - 5 > def_stats.speed

                if skill:
                    nature = skill # Eventually the skill tuple will contain more information...
                    if nature == 'physical':
                        damage = calculate_attack(attacker_ID, self.world) - def_stats.defense
                    elif nature == 'magical':
                        damage = calculate_magic_attack(attacker_ID, self.world) - def_stats.resistance
                else:
                    # Hitting a monster with the item will always deal physical damage.
                    # Future exceptions: wands could use charges to zap.
                    damage = calculate_attack(attacker_ID, self.world) - def_stats.defense

                    if double_attack:
                        damage += damage # Deal double damage
                    
                    # The defender counter attacks, unless it's furniture...
                    if not counter_attack and not self.world.has_component(defender_ID, FurnitureComponent):
                        self.queue.put({'ent': defender_ID, 'defender_IDs': [attacker_ID], 'counter_attack': True})
                
                if damage > 0:
                    def_stats.hp -= damage
                
                def_ren = self.world.component_for_entity(defender_ID, RenderComponent)
                self.world.messages.append({'combat': (att_ren.char, att_ren.color, def_ren.char, def_ren.color, damage, counter_attack, double_attack, self.world.turn)})

                if not skill and not counter_attack:
                    self.world.get_processor(EnergyProcessor).queue.put({'ent': attacker_ID, 'bump_attack': True})

                if def_stats.hp <= 0:
                    self.world.get_processor(DeathProcessor).queue.put({'ent': defender_ID})