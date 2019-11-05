from _data import map, UI_COLORS

from components.item.skills import SkillsComponent
from components.name import NameComponent

def render_popup_menu(console_object, world):
    console = console_object[0]
    menus = world.popup_menus
    if not menus:
        return 0

    menu = menus[-1]
    
    console.draw_frame(x=menu.x, y=menu.y, width=menu.w, height=menu.h, title=menu.title, clear=True, fg=UI_COLORS['fg'], bg=UI_COLORS['bg'])

    # Render choices
    dy = 2
    for choice in menu.contents:        
        color_fg = UI_COLORS['text']
        if not choice.valid:
            color_fg = UI_COLORS['text_invalid']

        string = '(' + choice.key + ') ' + choice.name.capitalize()
        console.print(menu.x + 2, menu.y + dy, string, color_fg)
        dy += 1
        if choice.description:
            console.print(menu.x + 2, menu.y + dy, "    " + choice.description, color_fg)
            dy += 1
        
        for condition in choice.conditions:
            color = color_fg
            if not condition.valid:
                color = UI_COLORS['text_condition_unmet']
            console.print(menu.x + 2, menu.y + dy, "    " + condition.description, color)
            dy += 1
    
    if menu.include_esc:
        console.print(menu.x + 2, menu.y + menu.h - 2, '(ESC) Close menu', UI_COLORS['text'])

    if menu.include_description and menu.include_description.get('item'):
        item = menu.include_description['item']
        dy = 2
        
        # Print the name of the item.
        name = world.component_for_entity(item, NameComponent).name
        console.print(menu.w // 2, menu.y + dy, f"Name: {name.capitalize()}", UI_COLORS['text'])

        # Print the available skills of the item.
        skills = world.component_for_entity(item, SkillsComponent).skills
        for skill in skills:
            dy += 1

            # Turn the list of jobs into a human readable format.
            jobs_list = list(dict.fromkeys(skill.job_req))
            jobs = ""
            for j in jobs_list:
                jobs += j + ", "
            jobs = jobs[:-2]

            console.print(menu.w // 2 + 2, menu.y + dy, f"Skill: {skill.name} ({jobs})", UI_COLORS['text'])
        