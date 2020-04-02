import data.damage_types as DamageTypes
import esper

from _helper_functions import as_integer, generate_stats
from components.actor.actor import ActorComponent
from components.render import RenderComponent
from components.stats import StatsComponent
from components.furniture import FurnitureComponent
from processors.death import DeathProcessor
from processors.energy import EnergyProcessor
from processors.skill_progression import SkillProgressionProcessor
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
            damage_type = DamageTypes.PHYSICAL # Bump attacks are physical
            if skill:
                damage_type = skill.damage_type

            for defender_ID in defender_IDs:
                if not self.world.has_component(defender_ID, ActorComponent):
                    print('ERROR: Why is the entity attaking a non-actor?')
                    continue

                damage = 0
                def_ren = self.world.component_for_entity(defender_ID, RenderComponent)
                def_stats = generate_stats(defender_ID, self.world)

                double_attack = att_stats['speed'] - 5 > def_stats['speed']

                if damage_type == DamageTypes.PHYSICAL:
                    damage = att_stats['attack'] - def_stats['defense']
                elif damage_type == DamageTypes.MAGICAL:
                    damage = att_stats['magic'] - def_stats['resistance']
                elif damage_type == DamageTypes.HEAL:
                    damage = 0
                
                if double_attack and not skill:
                    damage += damage # Deal double damage
                
                if damage > 0:
                    self.world.component_for_entity(defender_ID, StatsComponent).hp -= damage
                else:
                    damage = 0
                
                if def_stats['hp'] <= 0:
                    self.world.get_processor(DeathProcessor).queue.put({'ent': defender_ID})
                    self.world.get_processor(SkillProgressionProcessor).queue.put({'ent': attacker_ID, 'skill': skill, 'ap_gain': 10})
                elif not (skill or counter_attack or self.world.has_component(defender_ID, FurnitureComponent)):
                    self.world.get_processor(EnergyProcessor).queue.put({'ent': attacker_ID, 'bump_attack': True})
                    # The defender may counter attack.
                    self.queue.put({'ent': defender_ID, 'defender_IDs': [attacker_ID], 'counter_attack': True})

                self.world.messages.append({'combat': (att_ren.char, att_ren.color_fg, def_ren.char, def_ren.color_fg, as_integer(damage), counter_attack, double_attack, self.world.turn)})
