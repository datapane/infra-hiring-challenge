import logging
from celery import Celery
from flask import Flask, request, url_for, jsonify

from src.config import config
from src.job import Job
from src.docker_sandbox import DockerSandbox, DockerSandboxLimits


logging.basicConfig(format='%(levelname)s - %(asctime)s - %(message)s',
                    level=logging.INFO)


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    return app


def create_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config["CELERY_RESULT_BACKEND"],
        broker=app.config["CELERY_BROKER_URL"]
    )
    celery.conf.update(app.config)
    return celery


app = create_app()
celery = create_celery(app)


##################
# Flask Routes ###
##################

@app.route('/run-file', methods=['POST'])
def run_file():
    data = request.data
    if data:
        task = run_code_in_sandbox.apply_async(args=[data.decode("utf-8")])
        return jsonify({}), 202, {'Location': url_for('status',
                                                      task_id=task.id)}


@app.route('/run-json', methods=['POST'])
def run_json():
    json_data = request.get_json()
    if json_data and 'code' in json_data:
        code = json_data['code']
        task = run_code_in_sandbox.apply_async(args=[code])
        return jsonify({}), 202, {'Location': url_for('status',
                                                      task_id=task.id)}


@app.route('/status/<task_id>')
def status(task_id):
    task = run_code_in_sandbox.AsyncResult(task_id)
    result = parse_task_result(task)
    return jsonify(result)


##################
# Celery tasks ###
##################

@celery.task(bind=True)
def run_code_in_sandbox(self, code):
    logging.info("Starting running celery task")
    docker_sandbox_limits = DockerSandboxLimits(
        app.config["SANDBOX_MAX_MEM"],
        app.config["SANDBOX_MAX_CPUS"],
        app.config["SANDBOX_RUN_TIMEOUT"]
    )

    sandbox = DockerSandbox(
        app.config["SANDBOX_DOCKER_IMAGE"],
        docker_sandbox_limits
    )
    job = Job(code)
    self.update_state(state=Job.JobStatus.RUNNING.name)
    finished_job = sandbox.run(job)
    return {
        "status": finished_job.status.name,
        "stdout": finished_job.stdout
    }


def parse_task_result(task):
    if task.state in ("PENDING", Job.JobStatus.RUNNING.name):
        result = {
            "status": Job.JobStatus.RUNNING.name
        }
    elif task.state != 'FAILURE':
        result = {
            "stdout": task.info.get('stdout', ''),
            "status": task.info.get('status', '')
        }
    else:
        result = {
            "status": Job.JobStatus.CRASHED.name,
        }
    return result


if __name__ == '__main__':
    app.run(debug=True)
