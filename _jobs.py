class Job:
    def __init__(self, description, name, races, skills, upkeep):
        self.description = description  # Type: str
        self.name = name                # Type: str
        self.races = races              # Type: list
        self.skills = skills            # Type: dict {'job': number}
        self.upkeep = upkeep            # Type: dict {'stat': penalty value}
        

JOBS = {
    'soldier': Job(
        description="Baby's first job.",
        name='soldier', 
        races=('human',),
        skills={},
        upkeep={}
    ),
    'warrior': Job(
        description='Has access to more devastating skills.', # Not rly.
        name='warrior',
        races=('human',),
        skills={},
        upkeep={'magic': 1, 'speed': 2}
    ),
    'beserker': Job(
        description='Classic orc.',
        name='beserker',
        races=('orc',),
        skills={},
        upkeep={'speed': 1, 'hp': 1}
    ),
    'rogue': Job(
        description='A job for seasoned fighters.',
        name='rogue',
        races=('human', 'goblin'),
        skills={'soldier': 1},
        upkeep={'speed': 1, 'hp': 15}
    )
}