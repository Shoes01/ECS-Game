import esper

from _data import TICKS_PER_TURN
from components.actor.energy import EnergyComponent
from components.actor.player import PlayerComponent
from processors.cooldown import CooldownProcessor
from processors.render import RenderProcessor
from queue import Queue

class EnergyProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.queue = Queue()

    def process(self):
        while not self.queue.empty():
            event = self.queue.get()

            ent = event['ent']

            _bump_attack = event.get('bump_attack')
            _consume = event.get('consume')
            _descend = event.get('descend')
            _drop = event.get('drop')
            _move = event.get('move')
            _pick_up = event.get('pick_up')
            _remove = event.get('remove')
            _skill = event.get('skill')
            _wait = event.get('wait')
            _wear = event.get('wear')

            if _bump_attack:
                self.world.component_for_entity(ent, EnergyComponent).energy += 1
            elif _consume:
                self.world.component_for_entity(ent, EnergyComponent).energy += 1
            elif _descend:
                self.world.component_for_entity(ent, EnergyComponent).energy += 1
            elif _drop:
                self.world.component_for_entity(ent, EnergyComponent).energy += 1
            elif _move:
                self.world.component_for_entity(ent, EnergyComponent).energy += 1
            elif _pick_up:
                self.world.component_for_entity(ent, EnergyComponent).energy += 1
            elif _remove:
                self.world.component_for_entity(ent, EnergyComponent).energy += 1
            elif _skill:
                self.world.component_for_entity(ent, EnergyComponent).energy += _skill
            elif _wait:
                self.world.component_for_entity(ent, EnergyComponent).energy += 1
            elif _wear:
                self.world.component_for_entity(ent, EnergyComponent).energy += 1
        
        # Prevent the ticker from ticking if the player is sitting at 0 energy (aka, hasn't acted yet).
        if self.world.component_for_entity(1, EnergyComponent).energy == 0:
            return 0

        self.world.ticker += 1

        if self.world.ticker % TICKS_PER_TURN == 0:
            self.world.turn += 1
            self.world.get_processor(CooldownProcessor).queue.put({'tick': True})

        for ent, (eng) in self.world.get_component(EnergyComponent):
            if eng.energy > 0:
                eng.energy -= 1
