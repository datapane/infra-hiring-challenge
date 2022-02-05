from enum import Enum


class Job:

    class JobStatus(Enum):
        NOT_STARTED = 0
        RUNNING = 1
        COMPLETED = 2
        CRASHED = 3
        TIMED_OUT = 4

    def __init__(self, code):
        self.code = code
        self.status = Job.JobStatus.NOT_STARTED
        self.stdout = ""

    def start(self):
        self.status = Job.JobStatus.RUNNING

    def crash(self):
        self.status = Job.JobStatus.CRASHED

    def time_out(self):
        self.status = Job.JobStatus.TIMED_OUT

    def complete(self):
        self.status = Job.JobStatus.COMPLETED
