FROM tiangolo/uwsgi-nginx-flask:python3.7

ADD . /todo

WORKDIR /todo

RUN pip install -r requirements.txt

# CMD ["python3","worker.py","0"]
