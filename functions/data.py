import os
import boto3
from dotenv import load_dotenv
load_dotenv()

def init_account_table():
    my_session = boto3.session.Session(
            aws_access_key_id=os.environ.get("ACCESS_KEY"),
            aws_secret_access_key=os.environ.get("SECRET_KEY"),
            region_name = "us-east-1",
        )

    return my_session.resource('dynamodb').Table("dfk-autoplayer-accounts")

def init_settings_table():
    my_session = boto3.session.Session(
            aws_access_key_id=os.environ.get("ACCESS_KEY"),
            aws_secret_access_key=os.environ.get("SECRET_KEY"),
            region_name = "us-east-1",
        )

    return my_session.resource('dynamodb').Table("dfk-autoplayer")

def init_tracking_table():
    my_session = boto3.session.Session(
            aws_access_key_id=os.environ.get("ACCESS_KEY"),
            aws_secret_access_key=os.environ.get("SECRET_KEY"),
            region_name = "us-east-1",
        )

    return my_session.resource('dynamodb').Table("dfk-buyer-tracking")

def get_accounts():
    accounts = []
    account_table = init_account_table()
    scan_response = account_table.scan(
            FilterExpression="enabled_manager = :enabled",
            ExpressionAttributeValues={
                ":enabled": True,
            })
    for item in scan_response["Items"]:
        accounts.append(item["address_"])
    return accounts