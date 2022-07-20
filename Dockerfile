FROM python:3.10.5
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/app
ADD innotter  ./
COPY requarements.txt ./
COPY entrypoint.sh ./

RUN pip install -r requarements.txt
RUN chmod +x entrypoint.sh
# ENTRYPOINT "entrypoint.sh"

