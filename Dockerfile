FROM python:3.10.5
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/app
ADD innotter  ./
COPY requarements.txt ./

RUN pip install -r requarements.txt



