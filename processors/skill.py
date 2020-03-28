import esper
import numpy as np

from _helper_functions import generate_stats
from components.actor.actor import ActorComponent
from components.actor.diary import DiaryComponent
from components.actor.equipment import EquipmentComponent
from components.actor.job import JobComponent
from components.item.skill_pool import SkillPoolComponent
from components.item.slot import SlotComponent
from components.name import NameComponent
from components.position import PositionComponent
from components.render import RenderComponent
from components.stats import StatsComponent
from components.tile import TileComponent
from data.components_master import SLOTS
from data.render import ENTITY_COLORS
from processors.combat import CombatProcessor
from processors.cooldown import CooldownProcessor
from processors.energy import EnergyProcessor
from processors.movement import MovementProcessor
from processors.render import RenderProcessor
from processors.state import StateProcessor
from queue import Queue

class SkillProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.queue = Queue()
        self._direction = None
        self._skill = None
        
    def process(self):
        while not self.queue.empty():
            event = self.queue.get()

            ent = event['ent']

            clear = event.get('skill_clear')
            confirm = event.get('skill_confirm')
            move = event.get('skill_move')
            skill_letter = event.get('skill_prepare')           

            if skill_letter:
                self._skill = self.find_skill(ent, skill_letter)
                self._direction = (1, 0)

                if self._skill:
                    results = self.get_tiles(ent)
                    self.highlight_tiles(results['tiles'])
                    self.world.get_processor(StateProcessor).queue.put({'skill_targeting': True})
                    self.world.get_processor(RenderProcessor).queue.put({'skill': self._skill, 'redraw': True})

            elif move:
                (dx, dy) = move
                self._direction = (dx, dy)
                results = self.get_tiles(ent)
                self.highlight_tiles(results['tiles'])
                
            elif confirm:
                self.queue.put({'ent': ent, 'skill_clear': True})
                if ent == 1:
                    results = self.get_tiles(ent)
                    self.do_skill(ent, self._direction, self._skill, results)
                else:
                    self.do_skill(ent, event['direction'], event['skill'], results) # This piece of code will never be used until monster AI understands skills.

            elif clear:
                if ent == 1:
                    results = self.get_tiles(ent)
                    self.unhighlight_tiles(results['tiles'])                    
                self._skill = None
                self._direction = None
                self.world.get_processor(StateProcessor).queue.put({'exit': True})
                self.world.get_processor(RenderProcessor).queue.put({'skill': False, 'redraw': True})

    def find_skill(self, ent, skill_letter):
        slot = SLOTS._key_to_slots[skill_letter]
        diary = self.world.component_for_entity(ent, DiaryComponent)
        skill = None

        # Check to see if the slot has an active skill.
        for s in diary.active:
            if s.slot == slot:
                skill = s
                break
        else:
            self.world.messages.append({'skill': ('no_skill_active', skill_letter, self.world.turn)})
            return 0

        # Check to see if the active skill is on cooldown.
        for entry in diary.cooldown:
            if skill == entry.skill and entry.remaining > 0:
                self.world.messages.append({'skill': ('on_cooldown', skill.name, self.world.turn)})
                return 0

        return skill

    def get_effect_array(self):
        x, y = self._direction
        hor, ver, direction = (None,)*3

        if   x ==  1: hor = 'east'
        elif x == -1: hor = 'west'
        
        if   y == -1: ver = 'north'
        elif y ==  1: ver = 'south'
        
        if hor and ver: direction = ver + '_' + hor
        elif hor:       direction = hor
        elif ver:       direction = ver

        array_east = np.array(self._skill.east)
        array_north_east = np.array(self._skill.north_east)

        if direction == 'east':
            return array_east
        elif direction == 'north':
            return np.rot90(array_east)
        elif direction == 'west':
            return np.rot90(np.rot90(array_east))
        elif direction == 'south':
            return np.rot90(np.rot90(np.rot90(array_east)))
        elif direction == 'north_east':
            return array_north_east
        elif direction == 'north_west':
            return np.rot90(array_north_east)
        elif direction == 'south_west':
            return np.rot90(np.rot90(array_north_east))
        elif direction == 'south_east':
            return np.rot90(np.rot90(np.rot90(array_north_east)))
    
    def get_tiles(self, ent):                
        array_of_effect = self.get_effect_array()
        pos = self.world.component_for_entity(ent, PositionComponent)
        xc, yc = pos.x, pos.y

        destination = None # ID
        targets = [] # [ID]
        tiles = {} # {ID: color_fg}
        blocked_tile = False     

        for y in range(0, array_of_effect.shape[1]):
            for x in range(0, array_of_effect.shape[0]):
                adjusted_x = xc + x - len(array_of_effect) // 2
                adjusted_y = yc + y - len(array_of_effect) // 2                
                entities = self.world.get_entities_at(adjusted_x, adjusted_y)
                number = array_of_effect[y][x]
                skill = 'skill_' + str(number)
                
                for entity in entities:
                    # Classify the entity first.
                    actor = False
                    floor = False
                    wall = False
                    
                    if self.world.has_component(entity, ActorComponent):
                        actor = True
                    elif self.world.has_component(entity, TileComponent):
                        if self.world.component_for_entity(entity, TileComponent).blocks_path:
                            wall = True
                        else:
                            floor = True
                    
                    ## COLOR LOGIC
                    tiles[entity] = ENTITY_COLORS.get(skill)

                    if number == 0 and (wall or floor):
                        tiles[entity] = None
                    elif number == 1:
                        pass    
                    elif number == 2 and wall:
                        tiles[entity] = ENTITY_COLORS['skill_blocked']
                    elif number == 3 and (actor or wall):
                        tiles[entity] = ENTITY_COLORS['skill_blocked']
                    elif number == 4 and (actor or wall):
                        tiles[entity] = ENTITY_COLORS['skill_blocked']
                    
                    ## COMBAT LOGIC
                    if number == 0:
                        pass
                    elif number == 1:
                        if actor:
                            targets.append(entity)
                    elif number == 2:
                        if actor:
                            targets.append(entity)
                        elif wall:
                            blocked_tile = True
                    elif number == 3:
                        if floor:
                            destination = entity
                        elif actor or wall:
                            blocked_tile = True
                    elif number == 4:
                        if actor or wall:
                            blocked_tile = True # This could be expanded to be more verbose!
        
        results = {
            'destination': destination, # Some skills, like a leap, have a final 'landing' tile.
            'blocked_tile': blocked_tile, # If this is False, then the skill won't fire. A single non-legal target is enough to stop the skill.
            'targets': targets, # List of entities being targeted by the skill.
            'tiles': tiles # List of tiles being targeted by the skill.
            }

        return results

    def highlight_tiles(self, tiles):
        for tile, color_fg in tiles.items():
            self.world.component_for_entity(tile, RenderComponent).color_highlight = color_fg

    def do_skill(self, ent, direction, skill_comp, results):
        # These are conditions under which the skill does not fire.
        if results['blocked_tile']:
            self.world.messages.append({'skill': ('blocked_tile', skill_comp.name, self.world.turn)})
            return 0
        elif not results['targets'] and not results['destination']:
            self.world.messages.append({'skill': ('no_legal_tile', skill_comp.name, self.world.turn)})
            return 0

        # Check to see if the costs can be paid.
        ent_stats = generate_stats(ent, self.world)
        insufficient_stats = []

        for stat, cost in skill_comp.cost_soul.items():
            if ent_stats[stat] < cost:
                insufficient_stats.append(stat)
        
        if insufficient_stats:
            error_message = ''
            for stat in insufficient_stats:
                error_message = error_message + str(stat) + ', '
            error_message = error_message[:-2]
            self.world.messages.append({'skill': (error_message, skill_comp.name, self.world.turn)})
            return 0
        
        # Pay the costs.
        self.world.get_processor(CooldownProcessor).queue.put({'ent': ent, 'register_skill': skill_comp})
        self.world.get_processor(EnergyProcessor).queue.put({'ent': ent, 'skill': skill_comp.cost_energy})
        ent_stats_comp = self.world.component_for_entity(ent, StatsComponent)
        for stat, cost in skill_comp.cost_soul.items():
            ent_stats_comp.__dict__[stat] -= cost
    
        # Fire the skill!
        if results['targets']:            
            self.world.get_processor(CombatProcessor).queue.put({'ent': ent, 'defender_IDs': results['targets'], 'skill': skill_comp})
        elif results['destination']:
            tile_pos = self.world.component_for_entity(results['destination'], PositionComponent)
            ent_pos = self.world.component_for_entity(ent, PositionComponent)
            dx = tile_pos.x - ent_pos.x
            dy = tile_pos.y - ent_pos.y
            self.world.get_processor(MovementProcessor).queue.put({'ent': ent, 'move': (dx, dy), 'skill': skill_comp})
            self.world.get_processor(EnergyProcessor).queue.put({'ent': ent, 'skill': skill_comp.cost_energy})
        
        self.world.messages.append({'skill': (None, skill_comp.name, self.world.turn)})

    def unhighlight_tiles(self, tiles):
        for tile, _ in tiles.items():
            self.world.component_for_entity(tile, RenderComponent).color_highlight = None