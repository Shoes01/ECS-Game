import esper
import tcod as libtcod

from _helper_functions import calculate_power
from components.actor.actor import ActorComponent
from components.actor.combat import CombatComponent
from components.actor.dead import DeadComponent
from components.actor.equipment import EquipmentComponent
from components.actor.stats import StatsComponent
from components.item.modifier import ModifierComponent
from components.render import RenderComponent

class CombatProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        for ent, (act, com, att_ren) in self.world.get_components(ActorComponent, CombatComponent, RenderComponent):
            attacker_ID = ent
            defender_ID = self.world.component_for_entity(attacker_ID, CombatComponent).defender_IDs.pop()

            if not self.world.has_component(defender_ID, ActorComponent):
                return 0
            
            defender_stats = self.world.component_for_entity(defender_ID, StatsComponent)

            damage = calculate_power(attacker_ID, self.world)

            defender_stats.hp -= damage

            def_ren = self.world.component_for_entity(defender_ID, RenderComponent)

            self.world.messages.append({'combat': (att_ren.char, att_ren.color, def_ren.char, def_ren.color, damage, self.world.turn)})

            if defender_stats.hp <= 0 and not self.world.has_component(defender_ID, DeadComponent):
                self.world.add_component(defender_ID, DeadComponent(murderer=attacker_ID))