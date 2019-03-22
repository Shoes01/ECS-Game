import esper
import tcod as libtcod

from components.actor import ActorComponent
from components.game.state import StateComponent
from components.player import PlayerComponent
from components.position import PositionComponent
from components.render import RenderComponent
from components.tile import TileComponent
from components.turn import TurnComponent
from components.velocity import VelocityComponent

class InitialProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        if self.world._entities == {}:
            # Create game meta-entity. It is ID 1.
            game = self.world.create_entity()
            self.world.add_component(game, StateComponent())

            # Create the player entity. It is ID 2.
            player = self.world.create_entity()
            self.world.add_component(player, ActorComponent())
            self.world.add_component(player, PlayerComponent())
            self.world.add_component(player, PositionComponent(x=15, y=15))
            self.world.add_component(player, RenderComponent(char='@', color=libtcod.white))
            self.world.add_component(player, TurnComponent())