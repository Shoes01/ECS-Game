import attr

@attr.s(auto_attribs=True, slots=True)
class Render:
    char: str
    color_fg: str
    codepoint: str

#################
### Character ###
#################

" I won't be putting anything here, as I will be using sprites ... this is legacy stuff? lol. "

################
### FG Color ###
################

#################
### Codepoint ###
#################

SPRITES = {
    'blank': 0,
    'corpse': 480,
    'player': 126,
    # Entities defined in consumables.json
    'con_soul_jar': 818,
    # Used in data/equipment.py
    'eqp_boots': 744,
    'eqp_dagger': 896,
    'eqp_hammer': 933,
    'eqp_hammer_war': 966,
    'eqp_helmet': 705,
    'eqp_shield': 837,
    'eqp_sword': 898,
    'eqp_sword_great': 964,
    'eqp_sword_long': 928,
    # Entities defined in monsters.json
    'mon_demon': 191,
    'mon_goblin': 89,
    'mon_kobold': 314,
    'mon_orc': 91,
    'mon_rat': 287,
    'mon_zombie': 25,
    # Entities defined in other.json
    'other_chest': 388,
    # Entities defined in tiles.json
    'floor_stone': 51,
    'stairs': 195,
    'wall_stone': 554,
    'wall_stone_var_1': 555,
    'wall_stone_var_2': 556, 
    'wall_stone_var_3': 557,
    'wall_stone_topleft': 18,
    'wall_stone_top': 19,
    'wall_stone_topright': 20,
    'wall_stone_left': 50,
    'wall_stone_right': 52,
    'wall_stone_bottomleft': 82,
    'wall_stone_bottom': 83,
    'wall_stone_bottomright': 84,
    # None json defined entities
    'loot_plural': 200
}
