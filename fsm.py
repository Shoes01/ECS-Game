from processors.final import FinalProcessor

class GameStateMachine:
    def __init__(self, processor):
        self.state_processor = processor
        self.state = MainMenu(self.state_processor)

    def on_event(self, event):
        state_class = self.state.on_event(event)
        self.state = state_class(self.state_processor)

        return state_class

class State:
    def __init__(self, state_processor):
        self.state_processor = state_processor

    def on_event(self, event):
        pass

    def __str__(self):
        return self.__class__.__name__

class MainMenu(State):
    def on_event(self, event):
        if event.get('exit'):
            return MainMenu
        elif event.get('load_game'):
            return Game
        elif event.get('new_game'):
            return NewGame
        return MainMenu

class NewGame(State):
    def on_event(self, event):
        if event.get('popup'):
            self.state_processor.world.popup_menus.append(event['popup'])
            return PopupMenu
        elif event.get('start_game'):
            return Game
        return NewGame

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
        elif event.get('popup'):
            self.state_processor.world.popup_menus.append(event['popup'])
            return PopupMenu
        elif event.get('skill_targeting'):
            return SkillTargeting
        elif event.get('soul_state'):
            return SoulState
        elif event.get('view_character_sheet'):
            return ViewCharacterSheet
        elif event.get('view_log'):
            return ViewLog
        return Game

class ViewCharacterSheet(State):
    def on_event(self, event):
        if event.get('exit'):
            return Game
        return ViewCharacterSheet

class GameOver(State):
    def on_event(self, event):
        if event.get('exit'):
            return MainMenu
        return GameOver

class Look(State):
    def on_event(self, event):
        if event.get('exit'):
            return Game
        return Look

class PopupMenu(State):
    def on_event(self, event):
        if event.get('exit'):
            while self.state_processor.world.popup_menus:
                self.state_processor.world.popup_menus.pop()
            return self.state_processor.world.previous_state
        elif event.get('pop'):
            self.state_processor.world.popup_menus.pop()
            if self.state_processor.world.popup_menus:
                return PopupMenu
            else:
                return self.state_processor.world.previous_state
        elif event.get('popup'):
            self.state_processor.world.popup_menus.append(event['popup'])
            return PopupMenu
        return PopupMenu

class SkillTargeting(State):
    def on_event(self, event):
        if event.get('exit'):
            return Game
        return SkillTargeting

class SoulState(State):
    def on_event(self, event):
        if event.get('exit'):
            return Game
        return SoulState

class VictoryScreen(State):
    def on_event(self, event):
        if event.get('exit'):
            return MainMenu
        return VictoryScreen

class ViewLog(State):
    def on_event(self, event):
        if event.get('exit'):
            return Game
        return ViewLog