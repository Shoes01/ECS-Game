import esper

from fsm import GameStateMachine
from queue import Queue

class StateProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.queue = Queue()
        self.state_machine = GameStateMachine()
        self.state_machine.state_processor = self

    def process(self):
        while not self.queue.empty():
            state = self.state_machine.on_event(self.queue.get()).__str__() # Only look at the string?
            self.world.state = state
