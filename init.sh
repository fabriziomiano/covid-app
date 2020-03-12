#!/bin/bash
set -e
echo "Starting SSH ..."
service ssh start
gunicorn -b 0.0.0.0:5000 covid:app
