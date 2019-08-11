import tcod as libtcod

from _data import LOG_COLORS
from components.actor.equipment import EquipmentComponent
from components.item.skill import ItemSkillComponent
from components.item.slot import SlotComponent
from components.name import NameComponent

def render_message_log(console_object, new_turn, world):        
    console, x, y, w, h = console_object
    
    # Draw the regular message log.
    console, x, y, w, h = world.consoles['log']
    if world.state == 'ViewLog':
        console, x, y, w, h = world.consoles['map']
    
    max_offset = len(world.messages) - h

    if world.messages_offset >= max_offset > 0:
        world.messages_offset = max_offset
        offset = -max_offset
    elif world.messages_offset <= 0:
        world.messages_offset = 0
        offset = None
    else:
        offset = -world.messages_offset
    
    if new_turn:
        try:
            world.messages.remove({'whitespace': True})
        except:
            pass
        world.messages.append({'whitespace': True})

    dy = h - 1
    offset_messages = world.messages[:offset]
    for message in reversed(offset_messages):
        _ai_awake = message.get('ai_awake')
        _combat = message.get('combat')
        _consume = message.get('consume')
        _death = message.get('death')
        _drop = message.get('drop')
        _error = message.get('error')
        _game_loaded = message.get('game_loaded')
        _game_saved = message.get('game_saved')
        _heal = message.get('heal')
        _max_hp = message.get('max_hp')
        _move_items = message.get('move_items')
        _pickup = message.get('pickup')
        _remove = message.get('remove')
        _skill = message.get('skill')
        _wear = message.get('wear')
        _whitespace = message.get('whitespace')

        if _ai_awake:
            char, color_fg, turn = _ai_awake
            
            libtcod.console_set_color_control(libtcod.COLCTRL_1, color_fg, libtcod.black)
            console.print(0, 0 + dy, '(Turn %s) %c%s%c wakes up!' % (turn, libtcod.COLCTRL_1, char, libtcod.COLCTRL_STOP), LOG_COLORS['warning'])

        elif _combat:
            att_char, att_color, def_char, def_color, damage, counter_attack, double_attack, turn = _combat

            libtcod.console_set_color_control(libtcod.COLCTRL_1, att_color, libtcod.black)
            libtcod.console_set_color_control(libtcod.COLCTRL_2, def_color, libtcod.black)
            if double_attack:
                double_attack = " twice!"
            else:
                double_attack = "."

            if counter_attack:
                console.print(0, 0 + dy, '(Turn %s) %c%s%c counter-attacks %c%s%c for %s%s' % (turn, libtcod.COLCTRL_1, att_char, libtcod.COLCTRL_STOP, libtcod.COLCTRL_2, def_char, libtcod.COLCTRL_STOP, damage, double_attack), LOG_COLORS['combat'])
            else:
                console.print(0, 0 + dy, '(Turn %s) %c%s%c hits %c%s%c for %s%s' % (turn, libtcod.COLCTRL_1, att_char, libtcod.COLCTRL_STOP, libtcod.COLCTRL_2, def_char, libtcod.COLCTRL_STOP, damage, double_attack), LOG_COLORS['combat'])
                

        elif _consume:
            name, success, turn = _consume

            if success:
                console.print(0, 0 + dy, '(Turn %s) You consume your %s.' % (turn, name), LOG_COLORS['success'])
            else:
                console.print(0, 0 + dy, '(Turn %s) You cannot consume your %s!' % (turn, name), LOG_COLORS['failure'])

        elif _death:
            char, color_fg, turn, is_furniture = _death

            libtcod.console_set_color_control(libtcod.COLCTRL_1, color_fg, libtcod.black)
            if is_furniture:
                console.print(0, 0 + dy, '(Turn %s) The %c%s%c is destroyed!' % (turn, libtcod.COLCTRL_1, char, libtcod.COLCTRL_STOP), LOG_COLORS['success'])
            else:
                console.print(0, 0 + dy, '(Turn %s) The %c%s%c has died!' % (turn, libtcod.COLCTRL_1, char, libtcod.COLCTRL_STOP), LOG_COLORS['death'])
        
        elif _drop:
            name, turn = _drop

            console.print(0, 0 + dy, '(Turn %s) You drop your %s.' % (turn, name), LOG_COLORS['success'])

        elif _error:
            message= _error

            console.print(0, 0 + dy, message, LOG_COLORS['error'])
        
        elif _game_loaded:
            console.print(0, 0 + dy, 'Game loaded.', LOG_COLORS['system_message'])
            
        elif _game_saved:
            console.print(0, 0 + dy, 'Game saved.', LOG_COLORS['system_message'])

        elif _heal:
            value, turn = _heal

            console.print(0, 0 + dy, '(Turn %s) You heal for %s point(s).' % (turn, value), LOG_COLORS['success'])
        
        elif _max_hp:
            value, turn = _max_hp

            console.print(0, 0 + dy, '(Turn %s) Your max hp increases by %s point(s).' % (turn, value), LOG_COLORS['success'])
        
        elif _move_items:
            turn, name, number = _move_items

            if name:
                console.print(0, 0 + dy, '(Turn %s) There is a %s here.' % (turn, name), LOG_COLORS['warning'])
            else:
                console.print(0, 0 + dy, '(Turn %s) There are %s items here.' % (turn, str(number)), LOG_COLORS['warning'])
                
        elif _pickup:
            name, success, turn = _pickup

            if success:
                console.print(0, 0 + dy, '(Turn %s) You pickup a %s.' % (turn, name), LOG_COLORS['success'])
            else:
                console.print(0, 0 + dy, '(Turn %s) There is nothing here to pick up.' % (turn), LOG_COLORS['failure'])

        elif _remove:
            name, success, turn = _remove

            if success:
                console.print(0, 0 + dy, '(Turn %s) You unequip your %s.' % (turn, name), LOG_COLORS['success'])
            else:
                console.print(0, 0 + dy, '(Turn %s) You are not wearing your %s!' % (turn, name), LOG_COLORS['failure'])

        elif _skill:
            error, name, turn = _skill

            if error == 'on_cooldown':
                console.print(0, 0 + dy, "(Turn %s) The %s's skill is on cooldown!" % (turn, name), LOG_COLORS['failure'])
            elif error == 'no_item':
                console.print(0, 0 + dy, '(Turn %s) No valid item found.' % (turn), LOG_COLORS['failure'])
            elif error == 'no_legal_item':
                console.print(0, 0 + dy, '(Turn %s) The %s has no skill.' % (turn, name), LOG_COLORS['failure'])
            elif error == 'no_legal_tile':
                console.print(0, 0 + dy, '(Turn %s) There is something in your way.' % (turn), LOG_COLORS['failure'])
            elif error == 'no_legal_target':
                console.print(0, 0 + dy, '(Turn %s) No valid target found.' % (turn), LOG_COLORS['failure'])
            elif error == 'no_error':
                console.print(0, 0 + dy, '(Turn %s) You use your %s skill!' % (turn, name), LOG_COLORS['success'])
            else:
                console.print(0, 0 + dy, '(Turn %s) You do not have enough %s points to use %s!' % (turn, error, name), LOG_COLORS['failure'])

        elif _wear:
            job = _wear.get('job')
            name = _wear.get('name')
            slot = _wear.get('slot')
            success = _wear.get('success')
            turn = _wear.get('turn')

            if success is True:
                console.print(0, 0 + dy, '(Turn %s) You equip your %s to your %s.' % (turn, name, slot), LOG_COLORS['success'])
            elif success == 'slot_filled':
                console.print(0, 0 + dy, '(Turn %s) You replace your %s item with your %s.' % (turn, slot, name), LOG_COLORS['success'])
            elif success == 'wrong_job':
                console.print(0, 0 + dy, '(Turn %s) You need to be a %s to equip your %s.' % (turn, job, name), LOG_COLORS['success'])
            else:
                console.print(0, 0 + dy, '(Turn %s) You cannot equip a %s!' % (turn, name), LOG_COLORS['failure'])

        elif _whitespace:
            # Do nothing. The dy still iterates.
            pass

        dy -= 1
        if dy < 0:
            break