FROM python:3.9.7-slim-buster

COPY . .

RUN pip install -r requirements.txt

CMD [ "gunicorn", "-c", "gunicorn.conf.py" ]