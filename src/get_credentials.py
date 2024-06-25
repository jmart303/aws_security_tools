import boto3
import get_aws_data

from boto3.session import Session


def get_credentials(func):
    def security_credentials(*args):
        func(*args)
        account = args[0]
        account_role = args[1]
        account_role_session_name = args[2]
        aws_access_key = args[3]
        aws_secret_access_key = args[4]
        aws_session_key = args[5]
        if (
                aws_access_key is None
                and aws_secret_access_key is None
                and aws_session_key is None
        ):
            sts_client = boto3.client("sts")
            assumed_role_object = sts_client.assume_role(
                RoleArn=f'arn:aws:iam::{account}{account_role}',
                RoleSessionName=account_role_session_name,
                DurationSeconds=3600,
            )
            credentials = assumed_role_object["Credentials"]
            return credentials
        else:
            func(*args)
            session = Session(
                aws_access_key_id=aws_access_key,
                aws_secret_access_key=aws_secret_access_key,
                aws_session_token=aws_session_key,
            )

            sts_client = session.client("sts")

            assumed_role_object = sts_client.assume_role(
                RoleArn=f'arn:aws:iam::{account}{account_role}',
                RoleSessionName="AssumeRoleISOAuditSession",
            )

            credentials = assumed_role_object["Credentials"]
            return credentials

    return security_credentials


@get_credentials
def get_creds(*args):
    account = args[0]
    logger = args[6]
    logger.info(f'getting credentials for {account}')


def security_credentials(target_account, security_role,
                         role, role_session_name, svcs_account, logger):
    access_key = None
    secret_access_key = None
    session_key = None
    audit_cred = get_creds(
        svcs_account,
        security_role,
        role_session_name,
        access_key,
        secret_access_key,
        session_key, logger
    )
    access_key = audit_cred["AccessKeyId"]
    secret_access_key = audit_cred["SecretAccessKey"]
    session_key = audit_cred["SessionToken"]
    creds = get_creds(
        target_account,
        role,
        role_session_name,
        access_key,
        secret_access_key,
        session_key, logger
    )

    return creds
