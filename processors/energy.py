import esper

from components.actor.actor import ActorComponent
from components.actor.combat import CombatComponent
from components.actor.energy import EnergyComponent
from components.actor.equip import EquipComponent
from components.actor.player import PlayerComponent
from components.actor.velocity import VelocityComponent
from components.actor.wait import WaitComponent

class EnergyProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        success = True
        for ent, (actor, eng) in self.world.get_components(ActorComponent, EnergyComponent):

            if self.world.has_component(ent, PlayerComponent) and eng.energy == 0:
                success = False

            if self.world.has_component(ent, CombatComponent):
                eng.energy += 10
                self.world.remove_component(ent, CombatComponent)
                success = True
            
            elif self.world.has_component(ent, EquipComponent):
                eng.energy += 10
                self.world.remove_component(ent, EquipComponent)
                success = True

            elif self.world.has_component(ent, VelocityComponent):
                eng.energy += 5
                self.world.remove_component(ent, VelocityComponent)
                success = True

            elif self.world.has_component(ent, WaitComponent):
                eng.energy += 1
                self.world.remove_component(ent, WaitComponent)
                success = True

        if success:
            for ent, (actor, eng) in self.world.get_components(ActorComponent, EnergyComponent):
                if eng.energy > 0:
                    eng.energy -= 1