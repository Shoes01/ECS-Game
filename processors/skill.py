import esper

from _data import ENTITY_COLORS
from components.actor.actor import ActorComponent
from components.actor.equipment import EquipmentComponent
from components.actor.skill_execute import SkillExecutionComponent
from components.actor.skill_prepare import SkillPreparationComponent
from components.item.skill import ItemSkillComponent
from components.item.slot import SlotComponent
from components.name import NameComponent
from components.position import PositionComponent
from components.render import RenderComponent
from components.tile import TileComponent
from processors.combat import CombatProcessor
from processors.energy import EnergyProcessor
from processors.movement import MovementProcessor
from processors.state import StateProcessor
from queue import Queue

class SkillProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.queue = Queue()
        self._item = None
        self._direction = None
        
    def find_item(self, ent, slot):
        eqp = self.world.component_for_entity(ent, EquipmentComponent)
        for item in eqp.equipment:
            if slot == self.world.component_for_entity(item, SlotComponent).slot and self.world.has_component(item, ItemSkillComponent):
                return item

    def get_direction_name(self, direction):
        # Fetch direction.
        x, y = direction
        hor = None
        ver = None
        direction = None

        if x == 1:
            hor = 'east'
        elif x == -1:
            hor = 'west'
        
        if y == -1:
            ver = 'north'
        elif y == 1:
            ver = 'south'
        
        if hor and ver:
            direction = ver + '_' + hor
        elif hor:
            direction = hor
        elif ver:
            direction = ver
        
        return direction

    def highlight_tiles(self, ent):
        item_comp = self.world.component_for_entity(self._item, ItemSkillComponent)
        named_direction = self.get_direction_name(self._direction)
        array_of_effect = item_comp.__dict__[named_direction]
        pos = self.world.component_for_entity(ent, PositionComponent)
        xc, yc = pos.x, pos.y

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
                        tile_component = self.world.component_for_entity(entity, TileComponent)
                        self.world.component_for_entity(entity, RenderComponent).highlight_color = ENTITY_COLORS.get(skill) # Color the tile; this will be undone of the number == 0

                        if tile_component.blocks_path:
                            wall = tile_component
                        else:
                            floor = tile_component

                    ### Figure out if the skill happens!
                    if number == 0: # This tile is not part of the skill.
                        if wall:
                            wall.highlight_color = None
                        elif floor:
                            floor.highlight_color = None
                    
                    elif number == 1: # This skill deals damage to entities.
                        pass

                    elif number == 2: # This skill deals damage to entities. This skill is blocked by terrain.
                        if wall:
                            self.world.component_for_entity(entity, RenderComponent).highlight_color = ENTITY_COLORS['skill_blocked']
                        
                    elif number == 3: # This skill moves the acting entity to this location. This skill is blocked by terrain.
                        if actor or wall:
                            self.world.component_for_entity(entity, RenderComponent).highlight_color = ENTITY_COLORS['skill_blocked']
                        
                    elif number == 4: # This skill does nothing on its own. This skill is blocked by terrain and actors.
                        if wall or actor:
                            self.world.component_for_entity(entity, RenderComponent).highlight_color = ENTITY_COLORS['skill_blocked']

    def do_skill(self, ent, direction, item):
        # Set the tiles to have their bg colors changes, and fetch the entities on those tiles.
        array_of_effect = self.world.component_for_entity(self._item, ItemSkillComponent).__dict__[self.get_direction_name(direction)]
        pos = self.world.component_for_entity(ent, PositionComponent)
        xc, yc = pos.x, pos.y
        
        entities_to_attack = []
        tile_destination = []
        legal_tile = True
        legal_target = False

        for y in range(0, array_of_effect.shape[1]):
            for x in range(0, array_of_effect.shape[0]):
                adjusted_x = xc + x - len(array_of_effect) // 2
                adjusted_y = yc + y - len(array_of_effect) // 2
                entities = self.world.get_entities_at(adjusted_x, adjusted_y)
                number = array_of_effect[y][x]
                
                for entity in entities:
                    # Classify the entity first.
                    actor = False
                    floor = False
                    wall = False
                    
                    if self.world.has_component(entity, ActorComponent):
                        actor = True

                    elif self.world.has_component(entity, TileComponent):
                        tile_component = self.world.component_for_entity(entity, TileComponent)

                        if tile_component.blocks_path:
                            wall = tile_component
                        else:
                            floor = tile_component

                    ### Figure out if the skill happens!
                    if number == 0: # This tile is not part of the skill.
                        pass
                    
                    elif number == 1: # This skill deals damage to entities.
                        if actor:
                            entities_to_attack.append(entity)
                            legal_target = True

                    elif number == 2: # This skill deals damage to entities. This skill is blocked by terrain.
                        if actor:
                            entities_to_attack.append(entity)
                        elif wall:
                            legal_tile = False
                            self.world.component_for_entity(entity, RenderComponent).highlight_color = ENTITY_COLORS['skill_blocked']
                        
                    elif number == 3: # This skill moves the acting entity to this location. This skill is blocked by terrain.
                        if floor:
                            tile_destination.append(entity)
                            legal_target = True
                        elif actor or wall:
                            legal_tile = False
                            self.world.component_for_entity(entity, RenderComponent).highlight_color = ENTITY_COLORS['skill_blocked']
                        
                    elif number == 4: # This skill does nothing on its own. This skill is blocked by terrain and actors.
                        if wall or actor:
                            legal_tile = False
                            self.world.component_for_entity(entity, RenderComponent).highlight_color = ENTITY_COLORS['skill_blocked']

    
        if entities_to_attack and legal_tile:
            # Do this skill!    
            self.world.get_processor(CombatProcessor).queue.put({'ent': ent, 'defender_IDs': entities_to_attack})
            self.world.get_processor(EnergyProcessor).queue.put({'ent': ent, 'skill': True})
        elif tile_destination and legal_tile:
            # Do this skill!
            tile = tile_destination.pop()
            tile_pos = self.world.component_for_entity(tile, PositionComponent)
            ent_pos = self.world.component_for_entity(ent, PositionComponent)
            dx = tile_pos.x - ent_pos.x
            dy = tile_pos.y - ent_pos.y
            self.world.get_processor(MovementProcessor).queue.put({'ent': ent, 'move': (dx, dy)})
            self.world.get_processor(EnergyProcessor).queue.put({'ent': ent, 'skill': True})

    def unhighlight_tiles(self, ent):
        array_of_effect = self.world.component_for_entity(self._item, ItemSkillComponent).__dict__[self.get_direction_name(self._direction)]
        entities = None
        pos = self.world.component_for_entity(ent, PositionComponent)
        xc, yc = pos.x, pos.y

        for y in range(0, 5): # TODO: Hope this is big enough!
            for x in range(0, 5):
                adjusted_x = xc + x - len(array_of_effect) // 2
                adjusted_y = yc + y - len(array_of_effect) // 2
                
                entities = self.world.get_entities_at(adjusted_x, adjusted_y)
        
        for entity in entities:
            if self.world.has_component(entity, TileComponent):
                self.world.component_for_entity(entity, RenderComponent).highlight_color = None

    def process(self):
        while not self.queue.empty():
            event = self.queue.get()

            ent = event['ent']

            slot = event.get('skill_prepare')
            move = event.get('skill_move')
            confirm = event.get('skill_confirm')
            clear = event.get('skill_clear')

            if slot:
                self._item = self.find_item(ent, slot)
                self._direction = (1, 0)
                if self._item:
                    self.highlight_tiles(ent)
                    self.world.get_processor(StateProcessor).queue.put({'skill_targeting': True})

            elif move:
                (dx, dy) = move
                self._direction = (dx, dy)
                self.highlight_tiles(ent)
                
            elif confirm:
                self.queue.put({'ent': ent, 'skill_clear': True})
                if ent == 1:
                    self.do_skill(ent, self._direction, self._item)
                else:
                    self.do_skill(ent, event['direction'], event['item'])

            elif clear:
                self.unhighlight_tiles(ent)
                self._item = None
                self._direction = None
                self.world.get_processor(StateProcessor).queue.put({'exit': True})
