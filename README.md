# Hub

python3 -m venv venv # create the virtualenv

source venv/bin/activate # activate the virtualenv

pip install -r requirements.txt # install the dependencies

service redis_6379 start # start redis

celery -A server_example.celery worker -l info  # starts the celery worker

gunicorn server_example:app # run hub server
