#!/bin/bash
source /etc/profile.d/conda.sh
conda activate url_shortener
export FLASK_APP=application
flask db migrate 
flask db upgrade
exec gunicorn --bind 0.0.0.0:5000 --access-logfile - --error-logfile - application:app
