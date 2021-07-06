#!/bin/bash

random-string() {
        cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w ${1:-32} | head -n 1
}
random=random-string
curl -X 'POST' \
  'http://url.k8s.singhjee.in/api/v1/urls/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"longUrl": "'$random'"}'
