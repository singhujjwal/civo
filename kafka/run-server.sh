#!/bin/bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8122
# curl -v http://127.0.0.1:8122/api/v1/kafka/ready/
