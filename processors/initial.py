import esper
import tcod as libtcod

from components.actor import ActorComponent
from components.game.event import EventComponent
from components.game.state import StateComponent
from components.persist import PersistComponent
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
        # Create game meta-entity. It is ID 1.
        self.world.create_entity(
            EventComponent(),
            PersistComponent(),
            StateComponent()
        )

        # Create the player entity. It is ID 2.
        self.world.create_entity(
            ActorComponent(),
            PersistComponent(),
            PlayerComponent(),
            PositionComponent(),
            RenderComponent(char='@', color=libtcod.white),
            TurnComponent()
        )

        self.world.remove_processor(InitialProcessor) # Only needs to be done once per session.