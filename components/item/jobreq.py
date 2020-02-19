import attr

@attr.s(auto_attribs=True, slots=True)
class JobReqComponent:
    ' Component represents a list of jobs that the using entity must belong to. '
    job_req: list = attr.Factory(list)