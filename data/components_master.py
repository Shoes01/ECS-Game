from components.actor.actor import ActorComponent
from components.actor.boss import BossComponent
from components.actor.brain import BrainComponent
from components.actor.corpse import CorpseComponent
from components.actor.diary import DiaryComponent
from components.actor.energy import EnergyComponent
from components.actor.equipment import EquipmentComponent
from components.actor.inventory import InventoryComponent
from components.actor.job import JobComponent
from components.actor.player import PlayerComponent
from components.actor.race import RaceComponent
from components.item.consumable import ConsumableComponent
from components.item.item import ItemComponent
from components.item.jobreq import JobReqComponent
from components.item.skill_pool import SkillPoolComponent
from components.item.slot import SlotComponent
from components.item.wearable import WearableComponent
from components.furniture import FurnitureComponent
from components.name import NameComponent
from components.persist import PersistComponent
from components.position import PositionComponent
from components.rarity import RarityComponent
from components.render import RenderComponent
from components.soul import SoulComponent
from components.stairs import StairsComponent
from components.stats import StatsComponent
from components.tile import TileComponent

# Actor Components
ACTOR = ActorComponent
BOSS = BossComponent
BRAIN = BrainComponent
CORPSE = CorpseComponent
DIARY = DiaryComponent
ENERGY = EnergyComponent
EQUIPMENT = EquipmentComponent
INVENTORY = InventoryComponent
JOB = JobComponent
PLAYER = PlayerComponent
RACE = RaceComponent

_actor_components = {'ACTOR': ACTOR, 'BOSS': BOSS, 'BRAIN': BRAIN, 'CORPSE': CORPSE, 'DIARY': DIARY, 'ENERGY': ENERGY, 'EQUIPMENT': EQUIPMENT, 'INVENTORY': INVENTORY, 'JOB': JOB, 'PLAYER': PLAYER, 'RACE': RACE}

# Item Components
CONSUMABLE = ConsumableComponent
ITEM = ItemComponent
JOB_REQ = JobReqComponent
SKILL_POOL = SkillPoolComponent
SLOT = SlotComponent
WEARABLE = WearableComponent

_item_components = {'CONSUMABLE': CONSUMABLE, 'ITEM': ITEM, 'JOB_REQ': JOB_REQ, 'SKILL_POOL': SKILL_POOL, 'SLOT': SLOT, 'WEARABLE': WEARABLE}

# Other Components
FURNITURE = FurnitureComponent
NAME = NameComponent
PERSIST = PersistComponent
POSITION = PositionComponent
RARITY = RarityComponent
RENDER = RenderComponent
SOUL = SoulComponent
STAIRS = StairsComponent
STATS = StatsComponent
TILE = TileComponent

_other_components = {'FURNITURE': FURNITURE, 'NAME': NAME, 'PERSIST': PERSIST, 'POSITION': POSITION, 'RARITY': RARITY, 'RENDER': RENDER, 'SOUL': SOUL, 'STAIRS': STAIRS, 'STATS': STATS, 'TILE': TILE}

all = {**_actor_components, **_item_components, **_other_components}