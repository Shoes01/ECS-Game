import attr

@attr.s(slots=True)
class JobReqComponent:
    ' Component represents a list of jobs that the using entity must belong to. '
    job_req: list = attr.ib(factory=list)