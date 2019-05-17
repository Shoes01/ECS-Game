from processors.final import FinalProcessor

class GameStateMachine:
    state_processor = None
    
    def __init__(self):
        self.state = MainMenu(self.state_processor)

    def on_event(self, event):
        state_class = self.state.on_event(event)
        self.state = state_class(self.state_processor)

        return self.state

class State:
    """
    We define a state object which provides some utility functions for the
    individual states within the state machine.
    """
    def __init__(self, state_processor):
        self.state_processor = state_processor

    def on_event(self, event):
        """
        Handle events that are delegated to this State.
        """
        pass

    def __repr__(self):
        """
        Leverages the __str__ method to describe the State.
        """
        return self.__str__()

    def __str__(self):
        """
        Returns the name of the State.
        """
        return self.__class__.__name__

class MainMenu(State):
    def on_event(self, event):
        if event.get('exit'):
            raise SystemExit(1)
        elif event.get('generate_map'):
            return Game

class Game(State):
    def on_event(self, event):
        if event.get('boss_killed'):
            return VictoryScreen
        elif event.get('exit'):
            self.state_processor.world.get_processor(FinalProcessor).queue.put({'reset_game': True})
            return MainMenu
        elif event.get('look'):
            return Look
        elif event.get('player_killed'):
            return GameOver
        elif event.get('popup_menu'): # TODO: need an event for this
            return PopupMenu
        elif event.get('skill_targeting'):
            return SkillTargeting
        elif event.get('view_log'):
            return ViewLog

class GameOver(State):
    def on_event(self, event):
        if event.get('exit'):
            self.state_processor.world.get_processor(FinalProcessor).queue.put({'reset_game': True})
            return MainMenu

class Look(State):
    def on_event(self, event):
        if event.get('exit'):
            return Game

class PopupMenu(State):
    def on_event(self, event):
        if event.get('exit'): # TODO: When there are no more menus, this event needs to be sent.
            return Game

class SkillTargeting(State):
    def on_event(self, event):
        if event.get('exit'):
            return Game

class VictoryScreen(State):
    def on_event(self, event):
        if event.get('exit'):
            self.state_processor.world.get_processor(FinalProcessor).queue.put({'reset_game': True})
            return MainMenu

class ViewLog(State):
    def on_event(self, event):
        if event.get('exit'):
            return Game