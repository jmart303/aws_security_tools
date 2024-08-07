import boto3
import botocore.exceptions


def list_accounts(credentials, logger):
    account_list = []
    access_key = credentials['AccessKeyId']
    secret_access_key = credentials['SecretAccessKey']
    session_key = credentials['SessionToken']
    try:
        logger.info(f'gathering aws accounts...')
        org_client = boto3.client('organizations',
                                  aws_access_key_id=access_key,
                                  aws_secret_access_key=secret_access_key,
                                  aws_session_token=session_key
                                  )

        paginator = org_client.get_paginator('list_accounts')
        page_iterator = paginator.paginate()
        for page in page_iterator:
            for acct in page['Accounts']:
                if acct['Status'] != 'ACTIVE':
                    continue
                else:
                    account_id = acct['Id']
                    account_list.append(account_id)
        return account_list
    except botocore.exceptions.ClientError as error:
        logger.critical(f'error retrieving accounts {error}')

