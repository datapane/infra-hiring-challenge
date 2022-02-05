import unittest
import os
from .utils import read_python_file
from src.docker_sandbox import DockerSandbox, DockerSandboxLimits
from src.job import Job
from src.constants import DEFAULT_SANDBOX_RUN_TIMEOUT, \
    DEFAULT_SANDBOX_DOCKER_IMAGE, \
    DEFAULT_SANDBOX_MAX_MEM, \
    DEFAULT_SANDBOX_MAX_CPUS


class TestDockerSandbox(unittest.TestCase):

    def setUp(self):
        self.docker_sandbox_limits = DockerSandboxLimits(
            DEFAULT_SANDBOX_MAX_MEM,
            DEFAULT_SANDBOX_MAX_CPUS,
            DEFAULT_SANDBOX_RUN_TIMEOUT
        )

        self.sandbox = DockerSandbox(
            DEFAULT_SANDBOX_DOCKER_IMAGE,
            self.docker_sandbox_limits
        )
        self.example_scripts_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "example_scripts"
        )

    def test_run_success(self):
        filename = "success.py"
        expected_stdout = "b'1 2 2 3 3 3 4 4 4 4 5 5 5 5 5 '"
        path = os.path.join(self.example_scripts_dir, filename)
        code = read_python_file(path)
        job = self.sandbox.run(Job(code))
        self.assertEqual(job.status, Job.JobStatus.COMPLETED)
        self.assertEqual(expected_stdout, job.stdout)

    def test_run_key_error(self):
        filename = "key_error.py"
        partial_stdout = "KeyError"
        path = os.path.join(self.example_scripts_dir, filename)
        code = read_python_file(path)
        job = self.sandbox.run(Job(code))
        self.assertEqual(job.status, Job.JobStatus.CRASHED)
        self.assertIn(partial_stdout, job.stdout)

    def test_run_timed_out_error(self):
        self.docker_sandbox_limits.timeout = 2
        filename = "timed_out.py"
        path = os.path.join(self.example_scripts_dir, filename)
        code = read_python_file(path)
        job = self.sandbox.run(Job(code))
        self.assertEqual(job.status, Job.JobStatus.TIMED_OUT)
        self.assertFalse(job.stdout)
