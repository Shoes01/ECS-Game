import esper

from components.actor.job import JobComponent
from components.actor.race import RaceComponent
from processors.state import StateProcessor
from menu import PopupMenu, PopupChoice
from queue import Queue

class NewGameProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.queue = Queue()
    
    def process(self):
        while not self.queue.empty():
            event = self.queue.get()

            new_game = event.get('new_game')
            select_race = event.get('select_race')
            select_job = event.get('select_job')

            if new_game:
                ########
                # JOBS #
                ########

                ###### Human Jobs! ########################
                menu_human_jobs = PopupMenu(title='Choose a Job.', include_esc=False, auto_close=True)
                _processor = NewGameProcessor
                ## Soldier
                _name = 'Soldier'
                _key = 's'
                _result = {'select_race': 'human', 'select_job': 'soldier'}
                _description = 'A regular soldier.'

                menu_human_jobs.contents.append(PopupChoice(name=_name, key=_key,  processor=_processor, result=_result, description=_description))

                ## Thief
                _name = 'Thief'
                _key = 't'
                _result = {'select_race': 'human', 'select_job': 'thief'}
                _description = 'A regular thief.'

                menu_human_jobs.contents.append(PopupChoice(name=_name, key=_key,  processor=_processor, result=_result, description=_description))

                ###### Elf Jobs! ##########################
                menu_elf_jobs = PopupMenu(title='Choose a Job.', include_esc=False, auto_close=True)
                _processor = NewGameProcessor
                ## Rogue
                _name = 'Rogue'
                _key = 'r'
                _result = {'select_race': 'elf', 'select_job': 'rogue'}
                _description = 'A dashing rogue.'

                menu_elf_jobs.contents.append(PopupChoice(name=_name, key=_key,  processor=_processor, result=_result, description=_description))                

                #########
                # RACES #
                #########

                menu_race = PopupMenu(title='Choose a Race.', include_esc=False, auto_close=False)
                _processor = StateProcessor
                # Human!
                _name = 'Human'
                _key = 'h'
                _result = {'popup': menu_human_jobs}
                _description = 'A regular human being.'

                menu_race.contents.append(PopupChoice(name=_name, key=_key,  processor=_processor, result=_result, description=_description))
                # Elf!
                _name = 'Elf'
                _key = 'e'
                _result = {'popup': menu_elf_jobs}
                _description = 'A regular elf being.'

                menu_race.contents.append(PopupChoice(name=_name, key=_key,  processor=_processor, result=_result, description=_description))

                self.world.get_processor(StateProcessor).queue.put({'popup': menu_race})
            
            if select_race:
                self.world.component_for_entity(1, RaceComponent).race = select_race

            if select_job:
                self.world.component_for_entity(1, JobComponent).job = select_job
                # Now that a job has been selected, the game may begin.
                self.world.get_processor(StateProcessor).queue.put({'start_game': True})