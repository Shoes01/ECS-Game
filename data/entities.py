from collections import namedtuple

import attr
import data.brain as Brain
import data.components_master as Components
import data.render as Render
import data.skills as Skills
import data.souls as Souls
import data.stats as Stats

# ITEMS #######################################################################

' Base components that are the same to all Items. '
ITEM = {
    Components.ITEM: Components.ITEM(),
    Components.POSITION: (),
    Components.WEARABLE: Components.WEARABLE(),
}

HAMMER = {**ITEM,
    Components.JOB_REQ: (Components.JOBS.SOLDIER, Components.JOBS.WARRIOR),
    Components.NAME: 'Hammer',
    Components.RARITIES: Components.RARITIES.AWFUL,
    Components.RENDER: Render.HAMMER,
    Components.SLOTS: Components.SLOTS.MAINHAND,
    Components.STATS: Stats.HAMMER,
    Components.SKILL_POOL: [Skills.HEADBUTT, Skills.SPRINT]
}

SWORD = {**ITEM,
    Components.JOB_REQ: (Components.JOBS.SOLDIER, Components.JOBS.WARRIOR),
    Components.NAME: 'Sword',
    Components.RARITIES: Components.RARITIES.AWFUL,
    Components.RENDER: Render.SWORD,
    Components.SLOTS: Components.SLOTS.MAINHAND,
    Components.STATS: Stats.SWORD,
    Components.SKILL_POOL: [Skills.LUNGE, Skills.CLEAVE]
}

_all_items = {'HAMMER': HAMMER, 'SWORD': SWORD}

# ACTORS ######################################################################

' Base components that are the same to all Actors. '
ACTOR = {
    Components.ACTOR: Components.ACTOR(),
    Components.BRAIN: Brain.ZOMBIE,
    Components.DIARY: (),
    Components.ENERGY: (),
    Components.EQUIPMENT: (),
    Components.INVENTORY: (),
    Components.JOBS: Components.JOBS.MONSTER,
    Components.POSITION: (),
    Components.RACES: Components.RACES.MONSTER
}

DEMON = {**ACTOR,
    Components.NAME: 'Demon',
    Components.RARITIES: Components.RARITIES.MYTHIC,
    Components.RENDER: Render.DEMON,
    Components.SOUL: Souls.DEMON,
    Components.STATS: Stats.DEMON
}

PLAYER = {**ACTOR,
    Components.BRAIN: Brain.NONE,
    Components.JOBS: Components.JOBS.SOLDIER,
    Components.NAME: 'Player',
    Components.PERSIST: Components.PERSIST(),
    Components.PLAYER: Components.PLAYER(),
    Components.RACES: Components.RACES.HUMAN,
    Components.RENDER: Render.PLAYER,
    Components.SOUL: Souls.PLAYER,
    Components.STATS: Stats.PLAYER
}

ZOMBIE = {**ACTOR,
    Components.NAME: 'Zombie',
    Components.RARITIES: Components.RARITIES.AWFUL,
    Components.RENDER: Render.ZOMBIE,
    Components.SOUL: Souls.ZOMBIE,
    Components.STATS: Stats.ZOMBIE
}

_all_actors = {'DEMON': DEMON, 'PLAYER': PLAYER, 'ZOMBIE': ZOMBIE}

# CONSUMABLES #################################################################

' Base components that are the same to all Consumables. '
CONSUMABLE = {
    Components.CONSUMABLE: Components.CONSUMABLE(),
    Components.ITEM: Components.ITEM(),
    Components.POSITION: ()
}

SOUL_JAR = {**CONSUMABLE,
    Components.NAME: 'Soul Jar',
    Components.RENDER: Render.SOUL_JAR
}

_all_consumables = {'SOUL_JAR': SOUL_JAR}

# FURNITURE ###################################################################

' Base components that are the same to all Furniture. '
FURNITURE = {
    Components.ACTOR: Components.ACTOR(),
    Components.FURNITURE: Components.FURNITURE(),
    Components.POSITION: ()
}

CHEST = {**FURNITURE,
    Components.INVENTORY: (),
    Components.NAME: 'Chest',
    Components.RARITIES: Components.RARITIES.UNCOMMON,
    Components.RENDER: Render.CHEST,
    Components.STATS: Stats.CHEST
}

_all_furniture = {'CHEST': CHEST}

# TILES #######################################################################

' Base components that are the same to all Tiles. '
TILE = {
    Components.POSITION: (),
    Components.TILES: Components.TILES.FLOOR
}

FLOOR = {**TILE,
    Components.RENDER: Render.FLOOR
}

STAIRS = {**TILE,
    Components.RENDER: Render.STAIRS,
    Components.STAIRS: Components.STAIRS()
}

WALL = {**TILE,
    Components.RENDER: Render.WALL,
    Components.TILES: Components.TILES.WALL
}

_all_tiles = {'FLOOR': FLOOR, 'STAIRS': STAIRS, 'WALL': WALL}

all = {**_all_actors, **_all_consumables, **_all_furniture, **_all_items, **_all_tiles}
