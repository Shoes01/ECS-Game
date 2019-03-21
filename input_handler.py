import tcod as libtcod

def handle_keys(key):
    # These keys should always work, regardless of state
    if chr(key.c) == 'd' and key.lctrl:
        # Ctrl+d: toggle debug mode
        return {'debug_toggle': True}
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the game
        return {'exit': True}

    return handle_general_keys(key)
    
def handle_general_keys(key):
    # Movement keys
    movement = handle_generic_movement(key)
    if movement:
        return movement
    
    return {}

def handle_generic_movement(key):
    key_char = chr(key.c)

    if key.vk == libtcod.KEY_UP or key_char == 'k' or key.vk == libtcod.KEY_KP8:
        return {'move': (0, -1)}
    elif key.vk == libtcod.KEY_DOWN or key_char == 'j' or key.vk == libtcod.KEY_KP2:
        return {'move': (0, 1)}
    elif key.vk == libtcod.KEY_LEFT or key_char == 'h' or key.vk == libtcod.KEY_KP4:
        return {'move': (-1, 0)}
    elif key.vk == libtcod.KEY_RIGHT or key_char == 'l' or key.vk == libtcod.KEY_KP6:
        return {'move': (1, 0)}
    elif key_char == 'y' or key.vk == libtcod.KEY_KP7:
        return {'move': (-1, -1)}
    elif key_char == 'u' or key.vk == libtcod.KEY_KP9:
        return {'move': (1, -1)}
    elif key_char == 'b' or key.vk == libtcod.KEY_KP1:
        return {'move': (-1, 1)}
    elif key_char == 'n' or key.vk == libtcod.KEY_KP3:
        return {'move': (1, 1)}
    elif key_char == '.' or key.vk == libtcod.KEY_KP5:
        return {'wait': True}
    
    return {}