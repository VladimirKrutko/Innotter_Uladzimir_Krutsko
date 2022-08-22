from Statistics import GetStatistics
import boto3
import json
from microservices.AWS_SETTINGS import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
from datetime import datetime
from typing import Dict


statistic_class = GetStatistics()
AWS_BASE_STORAGE_BUCKET_NAME = 'test-function-uladzimir'
S3_RESOURCE = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
S3_BUCKET = S3_RESOURCE.Bucket(AWS_BASE_STORAGE_BUCKET_NAME)
DEFAULT_DATE = str(datetime.now().date())


async def load_statistic(date_json: Dict):
    date = date_json['date']
    json_user_data = statistic_class.get_user_statistics_by_date(date=date)
    byte_user_data = bytes(json.dumps(json_user_data).encode('UTF-8'))
    dateload = ''.join(date.split('-'))
    users_link = f'user_data/innotter_db/user_json/dataload={dateload}/users.json'
    S3_BUCKET.put_bject(Key=users_link, Body=byte_user_data)

    return {'status': 'OK'}






