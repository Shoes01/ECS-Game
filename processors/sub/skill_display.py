from _helper_functions import as_decimal
from data.render import LOG_COLORS

def render_skill_display(console_object, skill, world):
    console, _, _, w, h = console_object
    
    cost_turn_string = f"Turn Cost: {skill.cost_energy}"

    cost_soul_string = "Stat Cost: "
    for stat, cost in skill.cost_soul.items():
        cost_soul_string += f"{as_decimal(cost)} {stat}, "
    cost_soul_string = cost_soul_string[:-2] # Remove the ', ' at the end of the loop.

    console.print(0, 0, skill.name.capitalize(), LOG_COLORS['skill'])
    console.print(0, 1, cost_turn_string, LOG_COLORS['skill'])
    console.print(0, 2, cost_soul_string, LOG_COLORS['skill'])
    console.print_box(0, 4, w, h, skill.description, LOG_COLORS['skill'])
