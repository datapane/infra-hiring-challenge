# celery defaults
DEFAULT_CELERY_BROKER_URL = "redis://localhost:6379/"
DEFAULT_CELERY_RESULT_BACKEND = "redis://localhost:6379/"

# docker sandbox defaults
DEFAULT_SANDBOX_DOCKER_IMAGE = "python:3.9.10-slim-buster"
DEFAULT_SANDBOX_RUN_TIMEOUT = 20
DEFAULT_SANDBOX_MAX_CPUS = 1
# default memory in mb
DEFAULT_SANDBOX_MAX_MEM = 64
