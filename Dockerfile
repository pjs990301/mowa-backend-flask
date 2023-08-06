FROM python:3.11

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY app app

ENV FLASK_APP=app/__init__.py

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]