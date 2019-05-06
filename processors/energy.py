import esper

from components.actor.combat import CombatComponent
from components.actor.energy import EnergyComponent
from components.actor.player import PlayerComponent
from components.actor.skill_execute import SkillExecutionComponent
from queue import Queue

class EnergyProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.queue = Queue()

    def process(self):
        while not self.queue.empty():
            event = self.queue.get()

            ent = event['ent']

            _consume = event.get('consume')
            _descend = event.get('descend')
            _drop = event.get('drop')
            _move = event.get('move')
            _pick_up = event.get('pick_up')
            _remove = event.get('remove')
            _wear = event.get('wear')

            if _consume:
                self.world.component_for_entity(ent, EnergyComponent).energy += 10
            elif _descend:
                self.world.component_for_entity(ent, EnergyComponent).energy += 10
            elif _drop:
                self.world.component_for_entity(ent, EnergyComponent).energy += 10
            elif _move:
                self.world.component_for_entity(ent, EnergyComponent).energy += 10
            elif _pick_up:
                self.world.component_for_entity(ent, EnergyComponent).energy += 10
            elif _remove:
                self.world.component_for_entity(ent, EnergyComponent).energy += 10
            elif _wear:
                self.world.component_for_entity(ent, EnergyComponent).energy += 10

        for ent, (eng) in self.world.get_component(EnergyComponent):
            if self.world.has_component(ent, CombatComponent):
                if self.world.has_component(ent, SkillExecutionComponent):
                    eng.energy += self.world.component_for_entity(ent, SkillExecutionComponent).cost
                    self.world.remove_component(ent, SkillExecutionComponent)
                else:
                    eng.energy += 10
                self.world.remove_component(ent, CombatComponent)

        deincrement = True
        for ent, (eng, player) in self.world.get_components(EnergyComponent, PlayerComponent):
            if eng.energy == 0:
                self.world.redraw = True
                deincrement = False

        if deincrement:
            self.world.ticker += 1
            for ent, (eng) in self.world.get_component(EnergyComponent):
                if eng.energy > 0:
                    eng.energy -= 1