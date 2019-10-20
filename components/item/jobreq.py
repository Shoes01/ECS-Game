class JobReqComponent:
    def __init__(self, job_req):
        # This needs to be a list.
        self.job_req = job_req if type(job_req) == list else (job_req,)