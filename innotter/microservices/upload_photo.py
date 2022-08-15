from fastapi import FastAPI, File, Form
import requests
import boto3

app = FastAPI()

AWS_BASE_STORAGE = 'innotter-uladzimir-krutsko/user-image/'
AWS_ACCESS_KEY_ID = 'AKIA46GRRWDGRIFQIK7L'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'innotter-uladzimir-krutsko'
S3_RESOURCE = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
S3_BUCKET = S3_RESOURCE.Bucket(AWS_STORAGE_BUCKET_NAME)
USER_UPDATE_URL = 'http://127.0.0.1:8000/user/update/'


@app.post('/upload-image/')
def upload_image(image: bytes = File(...),
                 email: str = Form(...),
                 username: str = Form(...),
                 password: str = Form(...)):
    image_link = 'user-image' + '' + email.replace('.', '') + '-' + username + '.jpeg'
    print(image_link)
    image = image
    print(image)
    S3_BUCKET.put_object(Key=image_link, Body=image)
    user_data = {'user': {'email': email,
                          'username': username,
                          'password': password,
                          'image_s3_path': image_link}}

    req = requests.post(url=USER_UPDATE_URL, json=user_data)

    return req.json()
