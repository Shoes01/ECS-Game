class Job:
    def __init__(self, name, upkeep, races):
        self.name = name        # Type: str
        self.upkeep = upkeep    # Type: dict {'stat': penalty value}
        self.races = races      # Type: list

JOBS = {
    'soldier': Job(
        name='soldier', 
        upkeep={}, 
        races=('human',)
    ),
    'warrior': Job(
        name='warrior',
        upkeep={'magic': 1, 'speed': 2},
        races=('human',)
    ),
    'beserker': Job(
        name='beserker',
        upkeep={'speed': 1, 'hp': 1},
        races=('orc',)
    )
}