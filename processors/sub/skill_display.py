from _data import LOG_COLORS
from _helper_functions import as_decimal
from components.item.skills import SkillPoolComponent
from components.name import NameComponent


def render_skill_display(console_object, item, world):
    console, _, _, w, h = console_object
    item_name = world.component_for_entity(item, NameComponent).original_name
    skill = None
    for temp_skill in world.component_for_entity(item, SkillPoolComponent).skill_pool:
        if temp_skill.active:
            skill = temp_skill
    
    cost_turn_string = f"Turn Cost: {skill.cost_energy}"

    cost_soul_string = "Stat Cost: "
    for stat, cost in skill.cost_soul.items():
        cost_soul_string += f"{as_decimal(cost)} {stat}, "
    cost_soul_string = cost_soul_string[:-2] # Remove the ', ' at the end of the loop.

    console.print(0, 0, item_name, LOG_COLORS['skill'])
    console.print(0, 1, skill.name.capitalize(), LOG_COLORS['skill'])
    console.print(0, 2, cost_turn_string, LOG_COLORS['skill'])
    console.print(0, 3, cost_soul_string, LOG_COLORS['skill'])
    console.print_box(0, 5, w, h, skill.description, LOG_COLORS['skill'])
