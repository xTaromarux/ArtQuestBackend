#!/bin/bash
pip3 install virtualenv --user
python3 -m virtualenv venv
source venv/bin/activate
pip3 install -r app/requirements.txt
pip3 install -r app/ai_model/requirements.txt