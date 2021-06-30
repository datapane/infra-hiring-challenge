# Python Systems / Infrastructure Hiring Challenge

# Introduction

Datapane is an API-driven product for building analytics reports in Python - part of this includes running user's Python scripts and controlling their execution from a central server. This project simulates some of the necessary tasks required in developing such a system.

# Task

For this task we'll be building a simple API server with a few endpoints that reolve around accepting arbitary Python code and running it "securely".

The system must run on Linux, and can make use of any client/server technologies of your choice.

## Server

The API server supports a few endpoints.

`/run-file/`

this takes as a payload an uploaded python script containing the Python code to run

`/run-json/`

as per `run-file` above, but takes a JSON blob with a field called `code` containing the Python code to run

### Results

You may decide if the `/run-*` endpoints blocks and return a status code, or whether to implement an non-blocking model with a separate `/status/` endpoint to query each run. 

Either way, the server should listen for commands from client and act upon them - it should always be able to accept new messages.

## Running Code

You need to be able to run arbitrary Python code in a clean environment - i.e. each invocation should not affect the others. You will need to make decisions around venvs, installed libraries and dependencies, and more.

## Securing code

The uploaded Python code needs to be executed as securely as possible and handle code that may be hostile. As such you'll need to provide protections against user code that may attempt to use excess resources, e.g. time, space, cpu, etc.

You can look at any collection of technologies to perform sandboxing, such as systemd slices/scopes, podman, docker, chroots, seccomp filtering, and/or anything else

## Technologies

- Build systems, tools, and scripts of your choice, e.g. poetry, `setup.py`, docker, etc.
- The system must run on Linux and be simple to setup and run
- Any libraries you may find useful to help your task, we prioritise using existing libraries to accomplish tasks rather than building in-house and/or writing custom code that wouldn't scale to larger use-cases

## Requirements

- You do not need to worry about client/server service discovery - the locations of the systems can be hard-coded, provided as env vars, command-line parameters, etc.
- Instructions should be provided on how to build / bundle / start the system
- You should aim to use the latest Python language features, ecosystem, tooling, and libraries where possible

### Optional Features

- Defence is depth is a valid strategy, how many of the sandboxing techniques can be combined
- Consider how you would improve this approach and productise it - what issues do you foresee and how would you attempt to solve them
- Tests

# Review

Please don't spend more than 2-4 hours on this - we're looking to see how you approached the problem and the decisions made rather than a complete solution. This should be a fun challenge rather than a stressful endeavour.

There is no right answer as such, we will mainly be looking at code quality, software architecture skills, completeness of the solution from a software engineering perspective, and clarity of thought.

Once completed, please create a PR containing your work, send us an email, and schedule a [second follow-up interview](https://calendar.google.com/calendar/selfsched?sstoken=UU1sbG9QV1hfcHlGfGRlZmF1bHR8ODI1ZjRlZWJlZTY0ZTQ1ZTI4MzNkZThhOGQ5MjZkNzg).
