from processors.final import FinalProcessor

class GameStateMachine:
    def __init__(self):
        self.state = MainMenu()

    def on_event(self, event):
        self.state = self.state.on_event(event)

        return self.state

class State:
    """
    We define a state object which provides some utility functions for the
    individual states within the state machine.
    """
    def __init__(self):
        # print('Processing current state:', str(self)) # This is printed every time a State is changed.
        pass

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
            # Code can be added here to quit the game. TODO
            return Exit()
        elif event.get('generate_map'):
            return Game()
        return self

class Exit(State):
    def on_event(self, event):
        return self

class Game(State):
    def on_event(self, event):
        if event.get('boss_killed'):
            return VictoryScreen()
        elif event.get('exit'):
            self.world.get_processor(FinalProcessor).queue.put({'reset_game': True}) # TODO: this doesn't work
            return MainMenu()
        elif event.get('look'):
            return Look()        
        elif event.get('player_killed'):
            return GameOver()
        elif event.get('popup_menu'): # TODO: need an event for this
            return PopupMenu()
        elif event.get('skill_targeting'): # TODO: need an event for this
            return SkillTargeting()
        elif event.get('view_log'):
            return ViewLog()
        return self

class GameOver(State):
    def on_event(self, event):
        if event.get('exit'):
            self.world.get_processor(FinalProcessor).queue.put({'reset_game': True})
            return MainMenu()
        return self

class Look(State):
    def on_event(self, event):
        if event.get('exit'):
            return Game()
        return self

class PopupMenu(State):
    def on_event(self, event):
        if event.get('exit'): # TODO: When there are no more menus, this event needs to be sent.
            return Game()
        return self

class SkillTargeting(State):
    def on_event(self, event):
        if event.get('exit'):
            return Game()
        return self

class VictoryScreen(State):
    def on_event(self, event):
        if event.get('exit'):
            self.world.get_processor(FinalProcessor).queue.put({'reset_game': True})
            return MainMenu()
        return self

class ViewLog(State):
    def on_event(self, event):
        if event.get('exit'):
            return Game()
        return self