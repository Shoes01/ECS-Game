from _data import LOG_COLORS
from _helper_functions import as_decimal
from components.item.skill import ItemSkillComponent
from components.name import NameComponent


def render_skill_display(console_object, item, world):
    console, _, _, w, h = console_object
    item_name = world.component_for_entity(item, NameComponent)._name
    item_skill_component = world.component_for_entity(item, ItemSkillComponent)
    skill_name = item_skill_component.name
    skill_description = item_skill_component.description
    skill_energy_cost = item_skill_component.cost_energy
    skill_stat_costs = item_skill_component.cost_soul
    
    cost_turn_string = f"Turn Cost: {skill_energy_cost}"

    cost_soul_string = "Stat Cost: "
    for stat, cost in skill_stat_costs.items():
        cost_soul_string += f"{as_decimal(cost)} {stat}, "
    cost_soul_string = cost_soul_string[:-2] # Remove the ', ' at the end of the loop.

    console.print(0, 0, item_name, LOG_COLORS['skill'])
    console.print(0, 1, skill_name.capitalize(), LOG_COLORS['skill'])
    console.print(0, 2, cost_turn_string, LOG_COLORS['skill'])
    console.print(0, 3, cost_soul_string, LOG_COLORS['skill'])
    console.print_box(0, 5, w, h, skill_description, LOG_COLORS['skill'])
