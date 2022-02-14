# Setup
1. Build datapane-sandbox-base
 
`./script/build-base-dockerfile.sh`
 
2. Run the docker-compose file.

`docker-compose up`

3. Install newman:

`npm install -g newman`

4. Run automated postman tests.

`./test/test_all.sh`

## My solution

### Stack used

I'm using docker-compose and redis. I had initially thought about using kubernetes, but using a local registry container
can make things harder to set up. You have to tag the containers differently between minikube and dockerformac.

I also spent a bit of time trying to get networkpolicies to work, using calico on dockerformac, before realising it's a 
[known issue that it doesn't work](https://github.com/docker/for-mac/issues/4626).

Rather than not waste more time, I decided to use docker-compose to demonstrate the basic ideas.

My api docker container binds to the docker sock, allowing for the building and running of sandboxes to be kicked off 
from within the api container.

A bash script with curl commands is used to pylint the solution, run the solution and send the output and status of the run 
back to the api container.

It makes use of the linux `timeout` command to kill the script if it runs for longer than 20 seconds.

### The api endpoints

### /run-json

takes a json object of "code": "<base64_encoded_code>" and runs an id to check the status of.

### /run-file

takes a file upload object 

### /status/\<id\>

returns status of run id

### /output/\<id\>

get base64 encoded stdout of run id

## Base dockerfile

Speeds up apt install because apt update doesn't cache.

Defines a lesser privileged user to run the pip install for, in case a malicious library is used.

## Testing

The postman automated tests run using newman. This allows for full end to end testing of the process.

The file upload feature can't be automated as far as I know, because postman uses a "Select files" input instead 
of a text field which would allow for a postman environment variable to be used.

## A better approach

In a production setting, you could use the kubernetes api to start a k8s Job resource to run   
a docker image that was built using kaniko in the cluster.

A message queue would take the process creation away from the api to reduce load.

A way to garbage collect would be necessary. Re-using built containers for each user workspace 
would be beneficial.

In kubernetes, networkpolicy resource could be used to stop the running sandbox from communicating 
with the internet. This would stop things like crypto mining from happening.

I think having a separate k8s cluster for the sandboxes would be the most secure option. Then you could alter the network 
policy to allow for messages to be sent back through redis. The redis cluster should also be only for the sandbox.

Kubernetes can use cpu and memory limits to throttle the resource usage of requests.
