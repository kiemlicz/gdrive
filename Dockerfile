FROM debian:buster
# test use only

RUN apt-get update && \
    apt-get install -y python3-minimal python3-pip && \
    pip3 install --upgrade setuptools wheel

COPY gdrive/ /opt/gdrive
COPY setup.py /opt
COPY requirements-test.txt /opt
COPY requirements.txt /opt
COPY README.md /opt

WORKDIR /opt