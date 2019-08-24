class Job:
    def __init__(self, description, name, races, upkeep):
        self.description = description  # Type: str
        self.name = name                # Type: str
        self.races = races              # Type: list
        self.upkeep = upkeep            # Type: dict {'stat': penalty value}
        

JOBS = {
    'soldier': Job(
        description="Baby's first job.",
        name='soldier', 
        upkeep={}, 
        races=('human',)
    ),
    'warrior': Job(
        description='Has access to more devastating skills.', # Not rly.
        name='warrior',
        upkeep={'magic': 1, 'speed': 2},
        races=('human',)
    ),
    'beserker': Job(
        description='Classic orc.',
        name='beserker',
        upkeep={'speed': 1, 'hp': 1},
        races=('orc',)
    )
}