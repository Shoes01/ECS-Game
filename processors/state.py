import esper

from components.actor.player import PlayerComponent
from fsm import GameStateMachine
from processors.final import FinalProcessor
from queue import Queue

class StateProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.queue = Queue()
        self.state_machine = GameStateMachine()
    
    def process(self):
        while not self.queue.empty():
            event = self.queue.get()

            _boss_killed = event.get('boss_killed')
            _generate_map = event.get('generate_map')
            _view_log = event.get('view_log')

            if _boss_killed:
                self.world.state_stack.append('VictoryScreen')
            elif _generate_map:
                self.world.state_stack.append('Game')
            elif _view_log:
                self.world.state_stack.append('ViewLog')


            self.world.fsm_state = self.state_machine.on_event(event).__str__() # Only look at the string?

        if self.world.state == 'Game':
            if self.world.flag_pop_state:
                self.world.state_stack.pop()
                self.world.get_processor(FinalProcessor).queue.put({'reset_game': True})
            elif self.world.component_for_entity(1, PlayerComponent).killed:
                self.world.remove_component(1, PlayerComponent)
                self.world.state_stack.append('GameOver')
            elif self.world.cursor.active:
                self.world.state_stack.append('Look')
            elif self.world.popup_menus:
                self.world.state_stack.append('PopupMenu')
            elif self.world.toggle_skill_targeting:
                self.world.state_stack.append('SkillTargeting')
        
        elif self.world.state == 'GameOver':
            if self.world.flag_pop_state:
                self.world.state_stack.pop() # Pop to Game
                self.world.state_stack.pop() # Pop to MainMenu
                self.world.get_processor(FinalProcessor).queue.put({'reset_game': True})
                
        elif self.world.state == 'Look':
            if self.world.flag_pop_state:
                self.world.state_stack.pop()
                self.world.cursor.active = False
                
        elif self.world.state == 'MainMenu':                
            if self.world.flag_pop_state:
                self.world.state_stack.pop()
                
        elif self.world.state == 'PopupMenu':
            if not self.world.popup_menus:
                self.world.state_stack.pop()
            if self.world.flag_pop_state:
                self.world.state_stack.pop()
        
        elif self.world.state == 'SkillTargeting':
            if not self.world.toggle_skill_targeting:
                self.world.state_stack.pop()
        
        elif self.world.state == 'VictoryScreen':
            if self.world.flag_pop_state:
                self.world.state_stack.pop() # Pop to Game
                self.world.state_stack.pop() # Pop to MainMenu
                self.world.get_processor(FinalProcessor).queue.put({'reset_game': True})
                
        elif self.world.state == 'ViewLog':
            if self.world.flag_pop_state:
                self.world.state_stack.pop()       