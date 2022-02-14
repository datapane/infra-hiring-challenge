import base64
import os
import subprocess
import uuid

from flask import Flask, flash, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import redis

ALLOWED_EXTENSIONS = {'py'}

app = Flask(__name__)

r = redis.Redis(
        host='redis',
        password='password')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/run-file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "", 400
    file = request.files['file']
    if file.filename == '':
        return "", 400
    if file and allowed_file(file.filename):
        file_bytes = file.read()
        base64_bytes = base64.b64encode(file_bytes)
        id = run_code_base64(base64_bytes.decode('ascii'))
        if id == None:
            return "", 500
        return jsonify(id=id), 200


def run_code_base64(code64):
    id = str(uuid.uuid4())
    r.set("status-"+id, "RUNNING")
    subprocess.call(["./run_sandbox.sh", id, code64])
    return id

@app.route('/run-json', methods=['POST'])
def run_json():
    # check if the post request has the file part
    content = request.get_json(silent=True)
    if content["code"] is None:
        return "", 400
    code64 = content["code"]

    id = run_code_base64(code64)
    if id == None:
        return "", 500

    return jsonify(id=id), 200

@app.route('/status/<id>', methods=['POST', 'GET'])
def status(id):
    if request.method == 'GET':
        status = r.get("status-"+id)
        if status == None:
            return "", 404
        return jsonify(
            status=status.decode("utf-8"),
        )
    if request.method == 'POST':
        body = request.get_json(silent=True)
        if "output" in body:
            code_output = body["output"]
            r.set("output-"+id, code_output)
        r.set("status-"+id, body["status"])
        return "", 200

@app.route('/output/<id>', methods=['GET'])
def output(id):
    output = r.get("output-"+id)
    if output == None:
        return "", 404
    return jsonify(
        output=output.decode("utf-8"),
    )