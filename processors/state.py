import esper

from fsm import GameStateMachine, PopupMenu
from queue import Queue

class StateProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.queue = Queue()
        self.state_machine = GameStateMachine(self)

    def process(self):
        while not self.queue.empty():
            if self.world.state is not PopupMenu:
                self.world.previous_state = self.world.state
            self.world.state = self.state_machine.on_event(self.queue.get())
