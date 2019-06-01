import esper
import tcod as libtcod

from collections import Counter

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
            defender_IDs = event['defender_IDs']
            counter_attack = event.get('counter_attack')
            skill = event.get('skill')

            att_ren = self.world.component_for_entity(attacker_ID, RenderComponent)
            att_stats = generate_stats(attacker_ID, self.world)

            for defender_ID in defender_IDs:
                if not self.world.has_component(defender_ID, ActorComponent):
                    print('ERROR: Why is the entity attaking a non-actor?')
                    continue

                damage = 0
                def_ren = self.world.component_for_entity(defender_ID, RenderComponent)
                def_stats = generate_stats(defender_ID, self.world)

                double_attack = att_stats['speed'] - 5 > def_stats['speed']

                if skill:
                    nature = skill # Eventually the skill tuple will contain more information...
                    if nature == 'physical':
                        damage = att_stats['attack'] - def_stats['defense']
                    elif nature == 'magical':
                        damage = att_stats['magic'] - def_stats['resistance']
                else:
                    # Hitting a monster with the item will always deal physical damage.
                    # Future exceptions: wands could use charges to zap.
                    damage = att_stats['attack'] - def_stats['defense']

                    if double_attack:
                        damage += damage # Deal double damage
                
                if damage > 0:
                    self.world.component_for_entity(defender_ID, StatsComponent).hp -= damage
                
                if self.world.component_for_entity(defender_ID, StatsComponent).hp <= 0:
                    self.world.get_processor(DeathProcessor).queue.put({'ent': defender_ID})
                elif not (skill or counter_attack or self.world.has_component(defender_ID, FurnitureComponent)):
                    # The defender may counter attack.
                    self.world.get_processor(EnergyProcessor).queue.put({'ent': attacker_ID, 'bump_attack': True})
                    self.queue.put({'ent': defender_ID, 'defender_IDs': [attacker_ID], 'counter_attack': True})

                self.world.messages.append({'combat': (att_ren.char, att_ren.color, def_ren.char, def_ren.color, damage, counter_attack, double_attack, self.world.turn)})


def generate_stats(ent, world):
    ent_stats = world.component_for_entity(ent, StatsComponent).__dict__
    if not world.has_component(ent, EquipmentComponent):
        return ent_stats
    
    ent_stats = Counter(ent_stats)

    for item_id in world.component_for_entity(ent, EquipmentComponent).equipment:
        if world.has_component(item_id, StatsComponent):
            item_stats = Counter(world.component_for_entity(item_id, StatsComponent).__dict__)
            ent_stats.update(item_stats)

    return ent_stats
