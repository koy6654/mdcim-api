FROM python:3.7.7-alpine3.11

RUN mkdir -p /app
WORKDIR /app

COPY /app/requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

EXPOSE 5001

ENTRYPOINT ["python3", "app.py"]