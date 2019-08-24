class Job:
    def __init__(self, name, upkeep, races):
        self.name = name        # Type: str
        self.upkeep = upkeep    # Type: dict {'stat': penalty value}
        self.races = races      # Type: list

JOBS = {
    'soldier': Job(
        name='soldier', 
        upkeep={'magic': 10, 'resistance': 10}, 
        races=('human',)
    ),
    'warrior': Job(
        name='warrior',
        upkeep={'magic': 5, 'speed': 10},
        races=('human',)
    )
}