FROM python:3.6.13-slim-buster


# install the docker client to be able to run docker commands from this container
# we will expose the docker socket from
# the host using '-v /var/run/docker.sock:/var/run/docker.sock' arg
RUN apt update && \
    apt install -y wget && \
    wget https://download.docker.com/linux/static/stable/x86_64/docker-20.10.9.tgz && \
    tar xzvf docker-20.10.9.tgz && \
    cp docker/* /usr/bin/

# install redis
RUN apt install -y redis


# install our dependencies
COPY requirements.txt /
RUN pip install -r /requirements.txt


COPY . /app
WORKDIR /app
# FALSE if you don't want to run tests
# TRUE if you want to run them
ENV APP_TESTING FALSE

ENTRYPOINT ["./start.sh"]