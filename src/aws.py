from decouple import config
import boto3


def upload_to_aws(dest, val):
	BUCKET_NAME = 'hkmechkey'

	session = boto3.Session(
		aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
		aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY')
	)

	session.resource('s3').Object(BUCKET_NAME, dest).put(Body=val)


def download_from_aws(dest):
	BUCKET_NAME = 'hkmechkey'

	session = boto3.Session(
		aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
		aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY')
	)
	s3 = session.resource('s3')
	obj = s3.Object(BUCKET_NAME, dest)

	return obj.get()['Body'].read().decode('utf-8')

