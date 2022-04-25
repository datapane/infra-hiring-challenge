#import required packages
import os, json, docker, shutil, time
from xml.dom.expatbuilder import Namespaces

#from matplotlib.font_manager import json_load
from app import app
from flask import request, jsonify
from werkzeug.utils import secure_filename #utility which returns a secure version of the filename being uploaded


# Types of files allowed
ALLOWED_EXTENSIONS = set(['py'])

# Lists used by the endpoints
run_json = []
run_file = []

json_parent_directory = app.config['UPLOAD_FOLDER'] # Where the json uploads will be stored
default_dir = "default_dir" # where the requirement files are placed
root_dir = "/home/user/datapane-infra-challenge" # Root path of the project
client_directory = None
client_id = 0

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class ContainerException(Exception):
    def __init__(self, message='137'):
        # Call the base class constructor with the parameters it needs
        super(ContainerException, self).__init__(message)

def run_client_script(client_name, client_dir):
    """
    This is the default dockerfile used which will run the users' scripts
    It uses the datapane-py-slim image which was custom built from python:3.10-slim
    It has the required python packages, non-root user, venv and will install
    all the required packages from the user
    """
    dockerfile1 = f'''
FROM datapane-py-slim:1.0 AS runner
WORKDIR /usr/app
COPY --chown=python:python . .
USER 999
# Start app
ENV PYTHONUNBUFFERED=1
# activate virtual environment
ENV PATH="/usr/app/venv/bin:$PATH"

RUN pipreqs . --force
RUN pip3 install --no-cache-dir -r requirements.txt
CMD ["python3", "./main.py"]'''

    #print (dockerfile1)
    # Save the dockerfile value from above to a Dockerfile on the host machine.
    file = open(f"{client_dir}/Dockerfile", "w")
    file.writelines(dockerfile1)
    file.close()

    # Change to the user's directory
    os.chdir(client_dir)
    # Connect to the docker env on the host machine
    cli = docker.from_env()
    #while True:
    #    try:
    #        # Build the image ot be used by the user, setting resource limits as necessary
    #        log = cli.images.build(path='./', dockerfile='Dockerfile', tag=f'{client_name}', container_limits={'memory': '60MB'})
    #        #log = cli.images.build(path='./', dockerfile='Dockerfile', tag=f'{client_name}')
    #        for line in log:
    #            print (line)
    #        break
    #    except:
    #        print("Sorry, your image wasn't created, check if your cpu and memory are within the required limits")
    i, log = cli.images.build(path='./', dockerfile='Dockerfile', tag=f'{client_name}', container_limits={'memory': '60MB'})
    for line in log:
        print (line)

    cli = docker.from_env()
    # Run a container from the image that was just built, with the same resource limits.$
    log = cli.containers.run(image=f'{client_name}', mem_limit='60mb', auto_remove=True)
    #print(log)

@app.route('/run-file', methods=['POST'])
def upload_file():
    """
    The API endpoint POST request for where files are uploaded
    The API requests needs the following 2 fields; files[], and client
    files[] is a list object where the users can upload multiple files from their project
    but the initial script needs to be named main.py for this case.
    client is simple the clients' name that they want to use
    """
    # Change to the root directory
    #os.chdir(root_dir)
    os.chdir(os.path.expanduser(root_dir))
    # Check if any files have been uploaded and act accordingly
    if 'files[]' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp
    files = request.files.getlist('files[]') # get list of files being uploaded
    client_name = (request.form.get('client')) #get client name

    errors = {}
    success = False
    # Set client_dir to the upload folder and client's name
    client_dir = os.path.join(app.config['UPLOAD_FOLDER'], client_name)
    isExist = os.path.exists(client_dir) # check if client directory already exists
    if not isExist: # if it doesn't exist, create it
        print(os.getcwd())
        print(f'./{default_dir}, {client_dir}')
        shutil.copytree(default_dir, client_dir)
    for file in files:	# go through list of files
        # Check if filename is allowed
        if file and allowed_file(file.filename):
            # Returns a secure version of a file name
            filename = secure_filename(file.filename)
            # Save the client's project path
            client_path = os.path.join(client_dir, filename)
            file.save(client_path)
            success = True

        else:
            errors[file.filename] = 'File type is not allowed'
    # For testing purposes, check the time it takes to build and run the container needed
    start = time.time()
    run_client_script(client_name, client_dir)
    end = time.time()
    print(end-start)
    if success and errors:
        errors['message'] = 'File(s) successfully uploaded'
        resp = jsonify(errors)
        resp.status_code = 500
        return resp
    if success:
        resp = jsonify({'message' : 'Files successfully uploaded'})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify(errors)
        resp.status_code = 500
        return resp


@app.route('/run-json', methods=['POST'])
def upload_json():
    """
    The API endpoint POST request for where jsons are sent
    The API requests needs the following 3 fields; script_name, code to be run, and client
    script_name is the name of the script to be run, as of this time it needs to be main.py
    client is simply the clients' name that they want to use
    code is a list which the client needs to make sure is formatted properly, such as
    escaping quotes, backslah, tabs etc...
    """
    os.chdir(os.path.expanduser(root_dir))
    # Append the existing list with the incoming requests
    run_json.append(request.get_json())
    # Convert the incoming python object into a json string
    json_list = (json.dumps(run_json, indent=4, sort_keys=True))
    # Convert the above json string into a python dictionary
    # Not sure if this is the most efficient way?
    json_object = (json.loads(json_list))
    global client_id

    # Starting from 0, each time a new client sends their json it is saved to the json_parsed
    # variable and increments the id by 1
    json_parsed = (json_object[client_id])
    client_id+=1
    # Save the value of they keys from the json sent by the client
    json_extracted_code = (json_parsed['code'])
    client_name = (json_parsed['client'])
    json_extracted_script_name = (json_parsed['script_name'])
    client_directory = client_name

    # Setting the path of the clients' project directory
    path = os.path.join(json_parent_directory, client_directory)
    client_directory = os.path.join(app.config['UPLOAD_FOLDER'], client_name) # setting client directory
    # check if client directory already exists
    isExist = os.path.exists(client_directory)
    if not isExist: # if it doesn't exist, create it
        print(os.getcwd())
        print(f'./{default_dir}, {client_directory}')
        shutil.copytree(default_dir, client_directory)
    # Store the extracted code from the json to python_code
    python_code = ("\n".join(map(str, json_extracted_code)))
    # Get the full path of the script to save the code to
    client_path = os.path.join(path, json_extracted_script_name)
    textFile = open(client_path, 'w')
    # Write the extracted python code to a script
    textFile.write(python_code)
    textFile.close()
    # Build and run the image and container respectively, and time the process
    # for testing purposes
    start = time.time()
    run_client_script(client_name, client_directory)
    end = time.time()
    print(end-start)

    return 'OK', 200

# For testing purposes, no authentication is used to GET the json
@app.route('/run-json')
def get_json():
  return jsonify(run_json)

#@app.route('/run-file')
#def get_file():
#  return jsonify(run_file)


if __name__ == "__main__":
    app.run()
