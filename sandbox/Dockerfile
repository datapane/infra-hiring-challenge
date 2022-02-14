FROM datapane-sandbox:1.0 as build-env

ARG ID
ARG FILE_BASE_64

COPY --chown=datapane:datapane sandbox/* .

RUN echo $FILE_BASE_64 | base64 -d > runfile.py


RUN virtualenv venv --python=/usr/bin/python3.9
RUN . venv/bin/activate

RUN pip install pipreqs
RUN pipreqs .

RUN pip install -r requirements.txt



CMD ["./entrypoint.sh"]