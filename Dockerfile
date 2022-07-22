FROM python:3.10.5
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /usr/src/app
ADD innotter  ./
COPY requarements.txt ./
COPY entrypoint.sh /usr/src/app

RUN pip install -r requarements.txt
RUN chmod +x entrypoint.sh
RUN ./entrypoint.sh

