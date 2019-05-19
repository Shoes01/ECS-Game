import esper

from fsm import GameStateMachine
from queue import Queue

class StateProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.queue = Queue()
        self.state_machine = GameStateMachine(self)

    def process(self):
        while not self.queue.empty():
            self.world.state = self.state_machine.on_event(self.queue.get()).__str__() # Only look at the string?
