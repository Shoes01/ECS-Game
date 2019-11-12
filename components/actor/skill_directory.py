import attr

from typing import Dict, Tuple

@attr.s(slots=True, auto_attribs=True)
class SkillDirectoryComponent:
    ' Component that holds all the information regarding skills mastered. '
    skill_directory: Dict[str, Dict[str, Tuple[int, int]]] = attr.Factory(dict)