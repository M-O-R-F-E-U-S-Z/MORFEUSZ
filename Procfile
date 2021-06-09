web: gunicorn morfeusz.wsgi:application --log-file - --preload 
web: python src/manage.py test --liveserver=0.0.0.0:$PORT
