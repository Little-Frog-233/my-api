#!/bin/bash

work_path=$(dirname $0)

export FLASK_DEBUG=1

export FLASK_APP=${work_path}/../app.py

flask run --host=0.0.0.0 --port=8051