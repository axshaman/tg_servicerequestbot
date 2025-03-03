FROM python:3.9

WORKDIR /src
COPY req.txt /src
RUN pip install -r req.txt

COPY . /src

