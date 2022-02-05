import unittest
import os
import time
import requests
from .utils import read_python_file
from src.job import Job


class TestRunEndpoints(unittest.TestCase):

    def setUp(self):
        self.base_url = "http://localhost:8080"
        self.example_scripts_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "example_scripts"
        )

    def run_success_common(self, method):
        filename = "success.py"
        post_url = f"{self.base_url}/{method}"
        expected_stdout = "b'1 2 2 3 3 3 4 4 4 4 5 5 5 5 5 '"
        path = os.path.join(self.example_scripts_dir, filename)
        code = read_python_file(path)
        if method == "run-json":
            response = requests.post(post_url, json={"code": code})
        else:
            response = requests.post(post_url, data=code)
        self.assertEqual(response.status_code, 202)
        location = response.headers.get("Location")
        self.assertTrue(location)
        self.assertIn("status", location)
        attempts = 20
        for i in range(attempts):
            response = requests.get(location)
            json_obj = response.json()
            status = json_obj["status"]
            self.assertIn(
                json_obj["status"],
                (Job.JobStatus.RUNNING.name, Job.JobStatus.COMPLETED.name)
            )
            if status == Job.JobStatus.COMPLETED.name:
                self.assertEqual(expected_stdout, json_obj["stdout"])
                break
            time.sleep(1)
        else:
            self.assertTrue(None)

    def test_run_success_run_json(self):
        method = "run-json"
        self.run_success_common(method)

    def test_run_success_run_file(self):
        method = "run-file"
        self.run_success_common(method)
