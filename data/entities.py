from collections import namedtuple

import attr
import data.brain as Brain
import data.components_master as Components
import data.jobs as Jobs
import data.rarities as Rarities
import data.render as Render
import data.skills as Skills
import data.slots as Slots
import data.souls as Souls
import data.stats as Stats

# ITEMS #######################################################################

' Base components that are the same to all Items. '
ITEM = {
    Components.ITEM: (),
    Components.POSITION: (),
    Components.WEARABLE: (),
}

HAMMER = {**ITEM,
    Components.JOB_REQ: [Jobs.SOLDIER, Jobs.WARRIOR],
    Components.NAME: ('Hammer',),
    Components.RARITY: Rarities.AWFUL,
    Components.RENDER: Render.HAMMER,
    Components.SLOT: Slots.MAINHAND,
    Components.STATS: {Stats.ATK: 7},
    Components.SKILL_POOL: [Skills.HEADBUTT, Skills.SPRINT]
}

SWORD = {**ITEM,
    Components.JOB_REQ: [Jobs.SOLDIER, Jobs.WARRIOR],
    Components.NAME: ('Sword',),
    Components.RARITY: Rarities.AWFUL,
    Components.RENDER: Render.SWORD,
    Components.SLOT: Slots.MAINHAND,
    Components.STATS: {Stats.ATK: 5},
    Components.SKILL_POOL: [Skills.LUNGE, Skills.CLEAVE]
}

_all_items = {'HAMMER': HAMMER, 'SWORD': SWORD}

' The items will now bestow their slot onto their skills. '
for _, item in _all_items.items():
    for skill in item[Components.SKILL_POOL]:
        if skill.slot is not item[Components.SLOT]:
            print(f"Skill slot is {skill.slot}, but the item slot is {item[Components.SLOT]}. These should be the same.")

# ACTORS ######################################################################

' Base components that are the same to all Actors. '
ACTOR = {
    Components.ACTOR: (),
    Components.BRAIN: Brain.ZOMBIE,
    Components.DIARY: (),
    Components.ENERGY: (),
    Components.EQUIPMENT: (),
    Components.INVENTORY: (),
    Components.JOB: Jobs.MONSTER,
    Components.POSITION: (),
}

DEMON = {**ACTOR,
    Components.NAME: ('Demon',),
    Components.RARITY: Rarities.MYTHIC,
    Components.RENDER: Render.DEMON,
    Components.SOUL: Souls.DEMON,
    Components.STATS: Stats.DEMON
}

PLAYER = {**ACTOR,
    Components.BRAIN: Brain.NONE,
    Components.JOB: Jobs.SOLDIER,
    Components.NAME: ('Player',),
    Components.PLAYER: (),
    Components.RENDER: Render.PLAYER,
    Components.SOUL: Souls.PLAYER,
    Components.STATS: Stats.PLAYER
}

ZOMBIE = {**ACTOR,
    Components.NAME: ('Zombie',),
    Components.RARITY: Rarities.AWFUL,
    Components.RENDER: Render.ZOMBIE,
    Components.SOUL: Souls.ZOMBIE,
    Components.STATS: Stats.ZOMBIE
}

_all_actors = {'DEMON': DEMON, 'PLAYER': PLAYER, 'ZOMBIE': ZOMBIE}

# CONSUMABLES #################################################################

' Base components that are the same to all Consumables. '
CONSUMABLE = {
    Components.CONSUMABLE: (),
    Components.ITEM: (),
    Components.POSITION: ()
}

SOUL_JAR = {
    Components.NAME: {'name': 'Soul Jar'},
    Components.RENDER: Render.SOUL_JAR
}

_all_consumables = {'SOUL_JAR': SOUL_JAR}

# FURNITURE ###################################################################

' Base components that are the same to all Furniture. '
FURNITURE = {
    Components.ACTOR: (),
    Components.FURNITURE: (),
    Components.POSITION: ()
}

CHEST = {**FURNITURE,
    Components.INVENTORY: (),
    Components.NAME: ('Chest',),
    Components.RARITY: Rarities.UNCOMMON,
    Components.RENDER: Render.CHEST,
    Components.STATS: Stats.CHEST
}

_all_furniture = {'CHEST': CHEST}

# TILES #######################################################################

Tile = namedtuple('Tile', 'blocks_path blocks_sight', defaults=(False, False))

' Base components that are the same to all Tiles. '
TILE = {
    Components.POSITION: (),
    Components.TILE: Tile(blocks_path=False, blocks_sight=False)
}

FLOOR = {**TILE,
    Components.RENDER: Render.FLOOR
}

STAIRS = {**TILE,
    Components.RENDER: Render.STAIRS
}

WALL = {**TILE,
    Components.RENDER: Render.WALL,
    Components.TILE: Tile(blocks_path=True, blocks_sight=True)
}

_all_tiles = {'FLOOR': FLOOR, 'STAIRS': STAIRS, 'WALL': WALL}

all = {**_all_actors, **_all_consumables, **_all_furniture, **_all_items, **_all_tiles}
