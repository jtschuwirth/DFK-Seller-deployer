import os
import boto3
from dotenv import load_dotenv
load_dotenv()

client = boto3.client(
    'lambda',
    aws_access_key_id=os.environ.get("ACCESS_KEY"),
    aws_secret_access_key=os.environ.get("SECRET_KEY"),
    region_name = "us-east-1",
    )