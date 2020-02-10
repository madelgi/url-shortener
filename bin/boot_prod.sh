#!/bin/bash
source /etc/profile.d/conda.sh
conda activate url_shortener
pip install -e .
flask db migrate
flask db upgrade
exec gunicorn -b :5000 --access-logfile - --error-logfile - application:app
