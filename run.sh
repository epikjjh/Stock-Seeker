#!bin/bash

. env/bin/activate
uwsgi --http :8000 --module apiServer.wsgi &
cd frontend
npm start &