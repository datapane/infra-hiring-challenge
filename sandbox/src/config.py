import os
from src import constants


def parse_env_int(variable):
    result = os.getenv(variable)
    if result and result.isdigit():
        return int(result)
    return None


class Config:

    # celery env vars
    CELERY_BROKER_URL = os.getenv(
        "CELERY_BROKER_URL", constants.DEFAULT_CELERY_BROKER_URL)
    CELERY_RESULT_BACKEND = os.getenv(
        "CELERY_RESULT_BACKEND", constants.DEFAULT_CELERY_RESULT_BACKEND
    )

    # sandbox env vars
    SANDBOX_DOCKER_IMAGE = os.getenv(
        "SANDBOX_DOCKER_IMAGE", constants.DEFAULT_SANDBOX_DOCKER_IMAGE)
    SANDBOX_RUN_TIMEOUT = parse_env_int("SANDBOX_RUN_TIMEOUT") or constants.DEFAULT_SANDBOX_RUN_TIMEOUT
    SANDBOX_MAX_CPUS = parse_env_int("SANDBOX_MAX_CPUS") or constants.DEFAULT_SANDBOX_MAX_CPUS
    # default memory in mb
    SANDBOX_MAX_MEM = parse_env_int("SANDBOX_MAX_MEM") or constants.DEFAULT_SANDBOX_MAX_MEM


config = Config
