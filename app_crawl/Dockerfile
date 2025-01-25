FROM python:3.9.15
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR ./tour_collector
COPY ./requirement.txt /tour_collector/

RUN python -m pip install --upgrade pip
RUN /bin/sh -c pip install -r requirement.txt

COPY . /tour_collector/
