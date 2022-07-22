FROM python:3.10.5
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /usr/src/app

COPY upload_photo.py ./
COPY requarements.txt ./
RUN pip install -r requarements.txt
RUN  uvicorn upload_photo:app --reload --port 8080:8080

