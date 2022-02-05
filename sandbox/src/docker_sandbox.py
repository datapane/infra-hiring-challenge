import docker
import logging
import os
import requests
import shutil
import urllib3
import uuid


class DockerSandboxLimits:

    def __init__(self, max_memory, max_cpus, timeout):
        self.max_memory = max_memory
        self.max_cpus = max_cpus
        self.timeout = timeout


class DockerSandbox:

    def __init__(self, image, limits, docker_client=None):
        self.docker_client = docker_client or docker.from_env()
        self.image = image
        self.limits = limits
        self.docker_client.images.pull(image)

    def run(self, job, script_path_container="/usr/bin/main.py", docker_run_overrides=None):
        # generate a random folder that will be mounted as a volume in a docker container
        # the folder will contain the python script that will be executed inside the container
        dirname_container = os.path.dirname(script_path_container)
        filename_container = os.path.basename(script_path_container)
        dirname = self._create_random_directory()
        filename = os.path.join(dirname, filename_container)
        cmd_in_container = f"python {script_path_container}"
        container = None

        try:
            self._write_code_to_file(job.code, filename)
            docker_run_args = {
                "detach": True,
                "volumes": [f"{dirname}:{dirname_container}"],
                "cpu_count": self.limits.max_cpus,
                "mem_limit": f"{self.limits.max_memory}m",
            }
            if docker_run_overrides and isinstance(docker_run_overrides, dict):
                docker_run_args = {**docker_run_args, **docker_run_overrides}
            logging.info("Started job")
            job.start()
            container = self.docker_client.containers.run(self.image, cmd_in_container, **docker_run_args)
            resp = container.wait(timeout=self.limits.timeout)
            status_code = resp["StatusCode"]
            if status_code == 0:
                job.complete()
            else:
                job.crash()
            job.stdout = str(container.logs())

        except (requests.exceptions.ReadTimeout, urllib3.exceptions.ReadTimeoutError,
                requests.exceptions.ConnectionError):
            logging.warning("Container timed out")
            job.time_out()

        finally:
            shutil.rmtree(dirname)
            if container:
                container.remove(v=True, force=True)
            self.docker_client.close()
        return job

    def _write_code_to_file(self, code, filename):
        with open(filename, "w") as f:
            f.write(code)

    def _create_random_directory(self):
        dirname = os.path.join("/tmp", uuid.uuid4().hex)
        os.makedirs(dirname)
        return dirname
