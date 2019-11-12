import esper

from _data import ENTITY_COLORS
from _helper_functions import generate_stats
from components.actor.actor import ActorComponent
from components.actor.equipment import EquipmentComponent
from components.actor.job import JobComponent
from components.item.skills import SkillsComponent
from components.item.slot import SlotComponent
from components.name import NameComponent
from components.position import PositionComponent
from components.render import RenderComponent
from components.stats import StatsComponent
from components.tile import TileComponent
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
        self._item = None
        self._direction = None
        
    def process(self):
        while not self.queue.empty():
            event = self.queue.get()

            ent = event['ent']

            clear = event.get('skill_clear')
            confirm = event.get('skill_confirm')
            move = event.get('skill_move')
            slot = event.get('skill_prepare')

            if slot:
                self._item = self.find_item(ent, slot)
                self._direction = (1, 0)
                if self._item:
                    results = self.get_tiles(ent)
                    self.highlight_tiles(results['tiles'])
                    self.world.get_processor(StateProcessor).queue.put({'skill_targeting': True})
                    self.world.get_processor(RenderProcessor).queue.put({'item': self._item, 'redraw': True})

            elif move:
                (dx, dy) = move
                self._direction = (dx, dy)
                results = self.get_tiles(ent)
                self.highlight_tiles(results['tiles'])
                
            elif confirm:
                self.queue.put({'ent': ent, 'skill_clear': True})
                if ent == 1:
                    results = self.get_tiles(ent)
                    self.do_skill(ent, self._direction, self._item, results)
                else:
                    self.do_skill(ent, event['direction'], event['item'], results)

            elif clear:
                if ent == 1:
                    results = self.get_tiles(ent)
                    self.unhighlight_tiles(results['tiles'])                    
                self._item = None
                self._direction = None
                self.world.get_processor(StateProcessor).queue.put({'exit': True})
                self.world.get_processor(RenderProcessor).queue.put({'item': False, 'redraw': True})

    def find_item(self, ent, slot):
        eqp = self.world.component_for_entity(ent, EquipmentComponent)
        has_item = False
        name = None
        on_cooldown = False
        turn = self.world.turn

        for item in eqp.equipment:
            if slot == self.world.component_for_entity(item, SlotComponent).slot:
                name = self.world.component_for_entity(item, NameComponent).original_name
                for skill in self.world.component_for_entity(item, SkillsComponent).skills:
                    if skill.active:
                        if skill.cooldown_remaining == 0:
                            return item
                        else:
                            on_cooldown = True
                else:
                    has_item = True
                    legal_item = False                    
            else:
                has_item = False
                
        if on_cooldown:
            error = 'on_cooldown'
        elif has_item:
            error = 'no_legal_item'
        else:
            error = 'no_item'

        self.world.messages.append({'skill': (error, name, turn)})

    def get_direction_name(self, direction):
        x, y = direction
        hor, ver, direction = (None,)*3

        if   x ==  1: hor = 'east'
        elif x == -1: hor = 'west'
        
        if   y == -1: ver = 'north'
        elif y ==  1: ver = 'south'
        
        if hor and ver: direction = ver + '_' + hor
        elif hor:       direction = hor
        elif ver:       direction = ver
        
        return direction

    def get_tiles(self, ent):
        skill_comp = None
        for skill in self.world.component_for_entity(self._item, SkillsComponent).skills:
            if skill.active:
                skill_comp = skill
                
        array_of_effect = skill_comp.__dict__[self.get_direction_name(self._direction)]
        pos = self.world.component_for_entity(ent, PositionComponent)
        xc, yc = pos.x, pos.y

        destination = None # ID
        targets = [] # [ID]
        tiles = {} # {ID: color_fg}
        legal_target = True
        

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
                            legal_target = False
                    elif number == 3:
                        if floor:
                            destination = entity
                        elif actor or wall:
                            legal_target = False
                    elif number == 4:
                        if actor or wall:
                            legal_target = False # This could be expanded to be more verbose!
        
        results = {
            'destination': destination,
            'legal_target': legal_target,
            'targets': targets,
            'tiles': tiles
            }

        return results

    def highlight_tiles(self, tiles):
        for tile, color_fg in tiles.items():
            self.world.component_for_entity(tile, RenderComponent).highlight_color = color_fg

    def do_skill(self, ent, direction, item, results):
        error = 'no_error'
        name = self.world.component_for_entity(item, NameComponent).original_name
        turn = self.world.turn

        # These are conditions under which the skill does not fire.
        if not results['legal_target']:
            error = 'no_legal_target'
            self.world.messages.append({'skill': (error, name, turn)})
            return 0
        elif not results['targets'] and not results['destination']:
            error = 'no_legal_tile'
            self.world.messages.append({'skill': (error, name, turn)})
            return 0

        # Check to see if the costs can be paid.
        skill_comp = None
        for skill in self.world.component_for_entity(self._item, SkillsComponent).skills:
            if skill.active:
                skill_comp = skill

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
            self.world.messages.append({'skill': (error_message, name, turn)})
            return 0
        
        # Pay the costs.
        self.world.get_processor(CooldownProcessor).queue.put({'register_item': item, 'register_skill_component': skill_comp})
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
        
        self.world.messages.append({'skill': (error, name, turn)})

    def unhighlight_tiles(self, tiles):
        for tile, _ in tiles.items():
            self.world.component_for_entity(tile, RenderComponent).highlight_color = None