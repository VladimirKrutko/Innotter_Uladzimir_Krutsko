FROM python:3.10.5
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /app
COPY . /app/

# ADD innotter  ./
COPY requarements.txt /app/
# COPY entrypoint.sh /usr/src/app

RUN pip install -r requarements.txt
# RUN chmod +x entrypoint.sh
# RUN ./entrypoint.sh

RUN python manage.py makemigrations user
RUN python manage.py makemigrations page
RUN python manage.py migrate
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

