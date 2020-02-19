import esper
import numpy as np

from _data import Jobs, Races

from components.actor.job import JobComponent
from components.actor.race import RaceComponent
from components.soul import SoulComponent
from processors.state import StateProcessor
from menu import PopupMenu, PopupChoice, PopupChoiceResult
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
                # Jobs #
                ########

                ###### Human Jobs! ########################
                menu_human_jobs = PopupMenu(title='Choose a Job.', include_esc=False, auto_close=True)
                _processor = NewGameProcessor
                ## Soldier
                _name = 'Soldier'
                _key = 's'
                _result = {'select_race': Races.HUMAN, 'select_job': Jobs.SOLDIER}
                _description = 'A regular soldier.'
                _results = (PopupChoiceResult(result=_result, processor=_processor),)

                menu_human_jobs.contents.append(PopupChoice(name=_name, key=_key, results=_results, description=_description))

                ## Thief
                _name = 'Thief'
                _key = 't'
                _result = {'select_race': Races.HUMAN, 'select_job': Jobs.THIEF}
                _description = 'A regular thief.'
                _results = (PopupChoiceResult(result=_result, processor=_processor),)

                menu_human_jobs.contents.append(PopupChoice(name=_name, key=_key, results=_results, description=_description))

                ###### Elf Jobs! ##########################
                menu_elf_jobs = PopupMenu(title='Choose a Job.', include_esc=False, auto_close=True)
                _processor = NewGameProcessor
                ## Rogue
                _name = 'Rogue'
                _key = 'r'
                _result = {'select_race': Races.ELF, 'select_job': Jobs.ROGUE}
                _description = 'A dashing rogue.'
                _results = (PopupChoiceResult(result=_result, processor=_processor),)

                menu_elf_jobs.contents.append(PopupChoice(name=_name, key=_key, results=_results, description=_description))                

                #########
                # Races #
                #########

                menu_race = PopupMenu(title='Choose a Race.', include_esc=False, auto_close=False)
                _processor = StateProcessor
                # Human!
                _name = 'Human'
                _key = 'h'
                _result = {'popup': menu_human_jobs}
                _description = 'A regular human being.'
                _results = (PopupChoiceResult(result=_result, processor=_processor),)

                menu_race.contents.append(PopupChoice(name=_name, key=_key, results=_results, description=_description))
                # Elf!
                _name = 'Elf'
                _key = 'e'
                _result = {'popup': menu_elf_jobs}
                _description = 'A regular elf being.'
                _results = (PopupChoiceResult(result=_result, processor=_processor),)

                menu_race.contents.append(PopupChoice(name=_name, key=_key, results=_results, description=_description))

                self.world.get_processor(StateProcessor).queue.put({'popup': menu_race})
            
            if select_race:
                self.world.component_for_entity(1, RaceComponent).race = select_race
                # Add base values to the soul based on race.
                np_soul = np.zeros((2, 3), dtype=int, order='F')
                np_soul.fill(10)
                self.world.component_for_entity(1, SoulComponent).np_soul += np_soul

            if select_job:
                self.world.component_for_entity(1, JobComponent).job = select_job
                # # Add varied values to the soul based on job.
                self.world.component_for_entity(1, SoulComponent).np_soul += np.array([[50, 5, 5], [1, -5, 0]], dtype=int, order='F')
                # Now that a job has been selected, the game may begin.
                self.world.get_processor(StateProcessor).queue.put({'start_game': True})