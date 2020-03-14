class JobReqComponent:
    ' Component represents a list of jobs that the using entity must belong to. '
    def __init__(self, *args):
        self.job_req = list(args)
"""
import attr

@attr.s(auto_attribs=True, slots=True)
class JobReqComponent:
    ' Component represents a list of jobs that the using entity must belong to. '
    job_req: list = attr.Factory(list)
    """
