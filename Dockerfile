FROM python:3.9-slim

WORKDIR /app/f-log

COPY . /app

RUN pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 5000

# Define environment variable pointing to the app within the f-log directory
ENV FLASK_APP=app.py

CMD ["flask", "run", "--host=0.0.0.0"]
