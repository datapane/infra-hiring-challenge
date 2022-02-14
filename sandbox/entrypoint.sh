#!/bin/bash

pylint --errors-only runfile.py > lint-output
pylintResult=$?

OUTPUT="$(cat lint-output | base64)"

if [ $pylintResult -ne 0 ]; then

  curl --location --request POST "http://web_tier/status/$ID" \
    --header 'Content-Type: application/json' \
    --data-raw "{\"output\": \"$OUTPUT\", \"status\": \"LINT_FAILED\"}"
  exit
fi

timeout --preserve-status 20 python runfile.py > output
runResult=$?

echo "Pylint result $runResult"

if [ $runResult -eq 143 ]; then
  curl --location --request POST "http://web_tier/status/$ID" \
    --header 'Content-Type: application/json' \
    --data-raw "{\"output\": \"$OUTPUT\", \"status\": \"TIMEOUT\"}"
  exit
fi

STATUS="RUN_FAILED"
if [ $runResult -eq 0 ]; then
  STATUS="DONE"
fi

OUTPUT="$(cat output | base64)"

curl --location --request POST "http://web_tier/status/$ID" \
  --header 'Content-Type: application/json' \
  --data-raw "{\"output\": \"$OUTPUT\", \"status\": \"$STATUS\"}"
