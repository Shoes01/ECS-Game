class JobReqComponent:
    ' Component represents a list of jobs that the using entity must belong to. '
    def __init__(self, *args):
        self.job_req = list(args)
