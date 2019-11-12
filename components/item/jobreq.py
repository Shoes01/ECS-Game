import attr

@attr.s(slots=True, auto_attribs=True)
class JobReqComponent:
    ' Component represents a list of jobs that the using entity must belong to. '
    job_req: list = attr.Factory(list)