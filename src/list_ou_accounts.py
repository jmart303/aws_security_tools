import get_aws_service_client
import botocore.exceptions
import credentials
import setup_environment
import get_aws_data
import json
from datetime import datetime


def list_ou_accounts(parent, logger, audit_credentials):
    account_list = []
    try:
        client = get_aws_service_client.get_aws_client('organizations', 'us-east-1', audit_credentials,
                                                       logger)
        response = client.list_accounts_for_parent(
            ParentId=parent
        )

        for account in response['Accounts']:
            acct = account['Id']
            account_response = client.describe_account(
                AccountId=acct
            )
            account = account_response['Account']['Id']
            name = account_response['Account']['Name']
            status = account_response['Account']['Status']
            account_list.append(f'{account}, {name}, {status}')
        return account_list
    except botocore.exceptions.ClientError as e:
        logger.critical(f'error connecting to org services {parent} {e}')


# if __name__ == '__main__':
#     start = datetime.now()
#     log_file = f'./logs/list_ou_account.log'
#     logger_config = setup_environment.Logger(start, log_file)
#     logger = logger_config.conf_logger()
#     account_config = get_aws_data.GetAccounts(logger, 'master')
#     master_account = account_config.get_account()
#
#     audit_credentials = credentials.get_audit_credentials(master_account, logger)
#     """
#     import private json file of parent ous
#     """
#     with open('private/parent_ous.json', 'r') as file:
#         data = json.load(file)
#         for item in data['parent_ous']:
#             parent_id = item['parent_id']
#             account_data = list_ou_accounts(parent_id, logger, audit_credentials)
#             print(account_data)
