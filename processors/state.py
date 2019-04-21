import esper

from components.actor.player import PlayerComponent

class StateProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        if self.world.state == 'Exit':
            # This state signals the engine to turn off. There is no coming back.
            pass

        if self.world.state == 'Game':
            if self.world.pop_state:
                self.world.state_stack.pop()
                self.world.pop_state = False
                self.world.reset_game = True
            if self.world.component_for_entity(1, PlayerComponent).killed:
                self.world.remove_component(1, PlayerComponent)
                self.world.state_stack.append('GameOver')
            if self.world.popup_menus:
                self.world.state_stack.append('PopupMenu')
            if self.world.generate_map:
                self.world.generate_map = False
            if self.world.victory:
                self.world.victory = False
                self.world.state_stack.append('VictoryScreen')
            if self.world.view_log:
                self.world.view_log = False
                self.world.state_stack.append('ViewLog')
            if self.world.cursor.active:
                self.world.state_stack.append('Look')
        
        elif self.world.state == 'GameOver':
            if self.world.pop_state:
                self.world.state_stack.pop() # Pop to Game
                self.world.state_stack.pop() # Pop to MainMenu
                self.world.pop_state = False
                self.world.reset_game = True
                
        elif self.world.state == 'Look':
            if self.world.pop_state:
                self.world.state_stack.pop()
                self.world.pop_state = False
                self.world.cursor.active = False
                
        elif self.world.state == 'MainMenu':
            if self.world.generate_map:
                self.world.generate_map = False
                self.world.state_stack.append('Game')
            if self.world.pop_state:
                self.world.state_stack.pop()
                self.world.pop_state = False
                
        elif self.world.state == 'PopupMenu':
            if not self.world.popup_menus:
                self.world.state_stack.pop()
        
        elif self.world.state == 'VictoryScreen':
            if self.world.pop_state:
                self.world.state_stack.pop() # Pop to Game
                self.world.state_stack.pop() # Pop to MainMenu
                self.world.pop_state = False
                self.world.reset_game = True
                
        elif self.world.state == 'ViewLog':
            if self.world.pop_state:
                self.world.state_stack.pop()
                self.world.pop_state = False                