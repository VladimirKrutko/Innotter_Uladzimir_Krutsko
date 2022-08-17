from typing import Dict
from fastapi import FastAPI, File, Form
import boto3
import pika
import json

app = FastAPI()

AWS_BASE_STORAGE = 'innotter-uladzimir-krutsko/user-image/'
AWS_ACCESS_KEY_ID = 'AKIA46GRRWDGRIFQIK7L'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'innotter-uladzimir-krutsko'
S3_RESOURCE = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
S3_BUCKET = S3_RESOURCE.Bucket(AWS_STORAGE_BUCKET_NAME)
USER_UPDATE_URL = 'http://127.0.0.1:8000/user/update/'
RABBIT_HOST = 'localhost'


async def send_link(message: Dict):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='innotter', durable=True)
    channel.basic_publish(exchange='', routing_key='innotter', body=json.dumps(message))


@app.post('/upload-image/')
def upload_image(image: bytes = File(...),
                 email: str = Form(...),
                 username: str = Form(...)):
    image_link = 'user-image' + '' + email.replace('.', '') + '-' + username + '.jpeg'
    image = image
    S3_BUCKET.put_object(Key=image_link, Body=image)
    user_data = {'email': email,
                 'image_s3_path': image_link
                 }
    send_link(message=user_data)

    return {'status': 'OK'}
