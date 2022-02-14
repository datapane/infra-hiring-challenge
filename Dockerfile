FROM python:3.9

RUN apt-get update -y && \
    apt-get install -y python3-pip docker.io python-dev


WORKDIR /app

COPY sandbox sandbox

COPY web_tier .

RUN pip install -r requirements.txt

ENTRYPOINT [ "flask" ]

CMD [ "run",  "--host=0.0.0.0", "--port=80"]