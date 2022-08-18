from celery import shared_task
from post.models import Post
import boto3
from microservices.AWS_SETTINGS import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

SENDER = 'krutkovova00@gmail.com'
AWS_REGION = 'eu-central-1'
SUBJECT = '{} posted new post'
BODY_TEXT = 'See new post on {} page'
CLIENT = boto3.client('ses', region_name=AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY)


@shared_task()
def send_email(post_id):
	post = Post.objects.get(pk=post_id)
	post_email = post.page_id.owner.email
	emailing_list = [user.email for user in post.page_id.followers.all()]
