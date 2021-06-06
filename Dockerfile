FROM python:3.9-slim
COPY ./ /srv/DSI-Join-List/
WORKDIR /srv/DSI-Join-List/

RUN apt-get update
RUN apt-get install build-essential -y
RUN pip install -r requirements.txt

WORKDIR /srv/DSI-Join-List/src/
CMD python ./main.py