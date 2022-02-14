#!/bin/bash

TEST_DIR=$(dirname $0)

NON_BREAKING_64 = $(cat "$TEST_DIR"/test_file_non_breaking.py | base64)
BREAKING_64 = $(cat "$TEST_DIR"/test_file_breaks.py | base64)
TIMEOUT_CODE64 = $(cat "$TEST_DIR"/test_file_timeout.py | base64)

newman run "$TEST_DIR"/non_breaking_codeString.postman_collection.json --env-var code="$NON_BREAKING_64"
#newman run "$TEST_DIR"/non_breaking_file_upload.postman_collection.json --env-var
newman run "$TEST_DIR"/breaking_code_string.postman_collection.json --env-var breaking_code="$BREAKING_64"
newman run "$TEST_DIR"/timeout_code_string.postman_collection.json --env-var breaking_code="$TIMEOUT_CODE64"