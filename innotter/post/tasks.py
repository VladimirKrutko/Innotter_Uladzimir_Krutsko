import boto3
from page.models import Page
from celery import shared_task
from botocore.exceptions import ClientError
from microservices.AWS_SETTINGS import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

SENDER = 'krutkovova00@gmail.com'
AWS_REGION = 'eu-central-1'
SUBJECT = '{} posted new post'
BODY_TEXT = 'See new post on {} page'
CLIENT = boto3.client('ses', region_name=AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
CHARSET = "UTF-8"


@shared_task()
def send_email(page_id):
    page = Page.objects.gey(pk=page_id)
    # emailing_list = [user.email ]
    send_result = []
    for user in page.followers.all():
        try:
            response = CLIENT.send_email(
                Destination={
                    'ToAddresses': [
                        user.email,
                    ],
                },
                Message={
                    'Body': {
                        'Text': {
                            'Charset': CHARSET,
                            'Data': BODY_TEXT,
                        },
                    },
                    'Subject': {
                        'Charset': CHARSET,
                        'Data': SUBJECT,
                    },
                },
                Source=SENDER)
            send_result.append(response)
        except ClientError as e:
            None

    return send_result
