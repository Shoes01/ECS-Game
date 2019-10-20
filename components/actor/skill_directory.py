class SkillDirectoryComponent:
    def __init__(self, job='unemployed'):
        self.skill_directory = {job: {}} # This should be done elsewhere...

        """
        Usage Example:
        
        self.skill_directory = {
            'soldier': {
                'bash': (85, 100),
                'slash': (100, 100),
                'skill_name': (current_ap, max_ap)
            },
            'job_name': {

            }
        }

        """