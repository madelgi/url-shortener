#!/bin/bash
source /etc/profile.d/conda.sh
conda activate url_shortener
export FLASK_APP=application
flask db migrate
flask db upgrade
flask run --host 0.0.0.0 --port 5000
