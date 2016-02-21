FROM python:2-alpine

WORKDIR /cycles

RUN apk update && apk add \
    tcpdump

COPY requirements.txt *.py ./
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "cycles.py"]
