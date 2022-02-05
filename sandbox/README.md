# Sandbox in docker

A Python API to run untrusted code in secure, isolated Docker based sandboxes.

It runs python code inside a one-time Docker container. It uses the official python Docker api to communicate with Docker.

Because it runs untrusted code, it provides some protection by limiting the resources of the spawned docker sandboxes. The user can override some of the limits via 
Docker `--env` or `env-file`  arguments.

The docker runtime can also be changed to harden the security:

* [gVisor](https://gvisor.dev/)
* [Kata Containers](https://katacontainers.io/)

## Build

```
docker build -t datapane_infra:3.6 .
```


## Run
```
docker run -v /tmp/:/tmp -v /var/run/docker.sock:/var/run/docker.sock -p 8080:8080 -d datapane_infra:3.6
```

### Run tests
```
docker run --env APP_TESTING=TRUE --name mysandbox -v /tmp/:/tmp -v /var/run/docker.sock:/var/run/docker.sock -p 8080:8080 -d datapane_infra:3.6
```

### Available .env variables that can be overridden
```
CELERY_BROKER_URL
CELERY_RESULT_BACKEND
SANDBOX_DOCKER_IMAGE
SANDBOX_RUN_TIMEOUT
SANDBOX_MAX_CPUS
SANDBOX_MAX_MEM
```

## Cleanup
```
docker rm mysandbox --force
```