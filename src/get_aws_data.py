import json
import boto3
import botocore.exceptions
from boto3.session import Session


region_name = 'us-east-1'


class GetAccounts:
    def __init__(self, logger, account_type):
        self.logger = logger
        self.account_type = account_type

    def get_account(self):
        secret_name = "main_accounts"
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )
        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
        except botocore.exceptions.ClientError as error:
            self.logger.critical(f'client error getting main account {error}')
            raise error

        if self.account_type == 'svcs':
            account = get_secret_value_response['SecretString']
            formatted_account = json.loads(account)
            return formatted_account['svcs']
        if self.account_type == "gd":
            account = get_secret_value_response['SecretString']
            formatted_account = json.loads(account)
            return formatted_account['gd']
        if self.account_type == "dev":
            account = get_secret_value_response['SecretString']
            formatted_account = json.loads(account)
            return formatted_account['dev']
        if self.account_type == "master":
            account = get_secret_value_response['SecretString']
            formatted_account = json.loads(account)
            return formatted_account['master']
        else:
            return None


class GetRoles:
    def __init__(self, role, logger):
        self.role = role
        self.logger = logger

    def get_role(self):
        secret_name = "roles"
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )
        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
        except botocore.exceptions.ClientError as error:
            self.logger.critical(f'client error getting roles {error}')
            raise error

        if self.role == 'audit':
            account = get_secret_value_response['SecretString']
            formatted_account = json.loads(account)
            return formatted_account['audit']
        if self.role == "security_audit":
            account = get_secret_value_response['SecretString']
            formatted_account = json.loads(account)
            return formatted_account['security_audit']
        if self.role == "security_ir":
            account = get_secret_value_response['SecretString']
            formatted_account = json.loads(account)
            return formatted_account['security_ir']
        if self.role == "enforce_ir":
            account = get_secret_value_response['SecretString']
            formatted_account = json.loads(account)
            return formatted_account['enforce_ir']
        if self.role == "security_enforce":
            account = get_secret_value_response['SecretString']
            formatted_account = json.loads(account)
            return formatted_account['security_enforce']
        if self.role == "enforce":
            account = get_secret_value_response['SecretString']
            formatted_account = json.loads(account)
            return formatted_account['enforce']
        else:
            return None

