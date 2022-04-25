# Infra Hiring Challenge

This is my submissions to the Infra Hiring Challenge for the second interview for Datapane.

## Requirements
A docker environment, python3 and pipenv are all needed on the machine running this script.
## Setup

Use the package manager [pipenv] to install the necessary modules. Make sure you're in the [python-files directory] and run the following commands

```bash
pipenv shell
pipenv install
```

Edit the `app.py` file and set the directory you want to save the clients' projects to. This is for both endpoints.
Edit the `python-api.py` file and set the root directory to this project directory.

## Usage

```
python3 python-api.py
```

## Testing Uploads of files /run-file
Using any method of your choice such as curl or postman, send a POST request as shown below
```bash
curl --location --request POST 'http://localhost:5000/run-file' \
--form 'files[]=@"/home/rentan/main.py"' \
--form 'client="test-client"'
```


## Testing Uploads of json blob
```bash
curl --location --request POST 'http://localhost:5000/run-json' \
--header 'Content-Type: application/json' \
--data-raw '{
    "script_name" : "main.py",
    "client" : "new-company",
    "code" : 
    ["import flask, marshmallow, os, zipp, docker,time","print(\"hello world\")","os.chdir(\"/\")","print(os.getcwd())","print(\"goodbye world\")"]
}'
```


### Output
It should show the output of the script when completed

## Notes
### Security
As security precautions, the image and container being built and ran will have a `python` user to execute the script which has no root privileges.

The docker container is also run using namespaces isolation to prevent them from communicating with each other, as well as having virtual environments. 

Each client has their own project directory and container to be used.

The files being updated by the clients are also passed through a module to make sure the name is secure, as well as the size of the files being uploaded.

There is also an option to limit the memory and cpu usage.

For the time being only `.py` files are accepted

### Performance
A pre-built custom image called `datapane-py-slim` derived from `python:3.10-slim` was created, which had the necessary python3 modules installed, updated linux security packages, the python user created, and the necessary directories. 

The image being used can be changed if performance is not suitable.

The `runner` stage which uses this image only needs to switch to the python user, set env variable if needed, copy the clients' files, install the required python packages from those files, and run the main.py script

Execution is fairly fast as most of the time depends on the clients' script.

### Results
For the time being the results of the scripts are only shown on stdout. It wasn't clear from the task what is needed to be done.

## Improvements

Upon further understanding I realised that there could be a `/status` endpoint from which the client could check their results from. This was not implemented in time but in the future a simple client ID and cookie/key could be used. This would make sure clients' couldn't access each other's results.

Smaller docker images could be used as currently each invocation takes up 500mb.

Currently there is no limit to how long the python script can take to execute. 

With more time better logging could be implemented to identify why an image wasn't built or why a container failed to start such as exceeded the resource limits, failed scripts etc...
