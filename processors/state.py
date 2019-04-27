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
            if self.world.flag_pop_state:
                self.world.state_stack.pop()
                self.world.flag_reset_game = True
            elif self.world.component_for_entity(1, PlayerComponent).killed:
                self.world.remove_component(1, PlayerComponent)
                self.world.state_stack.append('GameOver')
            elif self.world.cursor.active:
                self.world.state_stack.append('Look')
            elif self.world.popup_menus:
                self.world.state_stack.append('PopupMenu')
            elif self.world.toggle_skill_targeting:
                self.world.state_stack.append('SkillTargeting')
            elif self.world.flag_victory:
                self.world.state_stack.append('VictoryScreen')
            elif self.world.flag_view_log:
                self.world.state_stack.append('ViewLog')
        
        elif self.world.state == 'GameOver':
            if self.world.flag_pop_state:
                self.world.state_stack.pop() # Pop to Game
                self.world.state_stack.pop() # Pop to MainMenu
                self.world.flag_reset_game = True
                
        elif self.world.state == 'Look':
            if self.world.flag_pop_state:
                self.world.state_stack.pop()
                self.world.cursor.active = False
                
        elif self.world.state == 'MainMenu':
            if self.world.flag_generate_map:
                self.world.state_stack.append('Game')
            elif self.world.flag_pop_state:
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
                self.world.flag_reset_game = True
                
        elif self.world.state == 'ViewLog':
            if self.world.flag_pop_state:
                self.world.state_stack.pop()       