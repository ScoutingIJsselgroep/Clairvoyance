FROM python:2.7

ENV KML_FILENAME 2022.kml

WORKDIR /pythonapp

ADD clairvoyance.py /
ADD . .

RUN pip install pyKML

VOLUME /pythonapp

EXPOSE 1337

CMD ["python2.7", "./clairvoyance.py"]