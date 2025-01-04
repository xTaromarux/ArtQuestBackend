#!/bin/bash
python3 -m virtualenv --no-download -p python3.8.10 venv
source venv/bin/activate
pip3 install -r app/requirements.txt
pip3 install -r app/ai_model/requirements.txt