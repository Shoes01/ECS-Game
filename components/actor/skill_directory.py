import attr

from _data import Job
from typing import Dict, Tuple

@attr.s(slots=True, auto_attribs=True)
class SkillDirectoryComponent:
    ' Component that holds all the information regarding skills mastered. '
    skill_directory: Dict[Job, Dict[str, Tuple[int, int]]] = attr.Factory(dict)