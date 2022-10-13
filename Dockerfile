FROM python:2.7

ARG JOTIHUNT_HOST
ENV JOTIHUNT_HOST https://jotihunt.scouting-ijsselgroep.nl

WORKDIR /pythonapp

ADD clairvoyance.py /
ADD . .

RUN pip install pyKML requests

VOLUME /pythonapp

EXPOSE 1337

CMD ["python2.7", "./clairvoyance.py"]