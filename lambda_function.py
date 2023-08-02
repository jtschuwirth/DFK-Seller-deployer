from functions.data import get_accounts, init_settings_table
from functions.lambda_client import client
import json

def handler(event, context):
    settings_table = init_settings_table()
    settings = settings_table.get_item(Key={"key_": "seller_settings"})["Item"]
    enabled = settings["enabled"]
    current_invocation = int(settings["current_invocation"])
    target_invocation = int(settings["target_invocations"])
    if not enabled: return "Seller is disabled"
    settings_table.update_item(
        Key={"key_": "seller_settings"},
        UpdateExpression="SET current_invocation = :current_invocation",
        ExpressionAttributeValues={
            ":current_invocation": current_invocation+1
        }
    )
    if target_invocation-1 <= current_invocation: 
        settings_table.update_item(
            Key={"key_": "seller_settings"},
            UpdateExpression="SET current_invocation = :current_invocation",
            ExpressionAttributeValues={
                ":current_invocation": 0
            }
        )
    c=0
    accounts_to_manage = []
    account_groups = []
    for account in get_accounts():
        if int(account, 16)%target_invocation != current_invocation: continue
        if c==10: 
            account_groups.append(accounts_to_manage)
            accounts_to_manage = []
            c=0
        accounts_to_manage.append(account)
        c+=1
    if len(accounts_to_manage) > 0:
        account_groups.append(accounts_to_manage)
    for account_group in account_groups:
        print(f"running accounts: {account_group}" )
        client.invoke(
            FunctionName='dfk-seller',
            InvocationType='Event',
            Payload= json.dumps({"users": account_group})
        )


    return "Done"