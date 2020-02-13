import attr

from _data import Job
from typing import Dict, Tuple

@attr.s(slots=True, auto_attribs=True)
class SkillDirectoryComponent:
    ' Component that holds all the information regarding skills mastered. '
    skill_directory: Dict[Job, Dict[str, Tuple[int, int]]] = attr.Factory(dict)

    """
    Shape

    { Job class: {skill name: (current AP, max AP)} }

    Example

    skill_directory = {
        Soldier: {
            'slash': (0, 100),
            'stab': (50, 100),
            'kick': (100, 100)
        },
        Warrior: {
            'slash': (0, 100)
        }
    }
    """