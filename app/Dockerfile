FROM python:3.9-slim

EXPOSE 8000

RUN apt-get update && apt-get upgrade -y && apt-get -y install gcc

RUN pip install --upgrade pip

RUN useradd -ms /bin/bash aiuser
USER aiuser
WORKDIR /home/aiuser

COPY --chown=aiuser:aiuser requirements.txt requirements.txt
COPY --chown=aiuser:aiuser . /home/aiuser

ENV PATH="/home/aiuser/.local/bin:${PATH}"

RUN pip install --user -r requirements.txt

COPY --chown=aiuser:aiuser . .