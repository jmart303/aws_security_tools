import boto3
from boto3.session import Session
import get_aws_data


def get_credentials(func):
    def iso_credentials(*args):
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
                RoleSessionName="AssumeSecuritySession",
            )

            credentials = assumed_role_object["Credentials"]
            return credentials

    return iso_credentials


@get_credentials
def get_creds(*args):
    account = args[0]
    access_key = args[3]
    logger = args[6]
    if not access_key:
        logger.info(f'getting credentials for Security role {account}')
    else:
        logger.info(f'getting credentials for audit/enforce role {account}')


def get_audit_credentials(account, logger):
    dev_account_config = get_aws_data.GetAccounts(logger, 'dev')
    dev_account = dev_account_config.get_account()
    role_config = get_aws_data.GetRoles('security_audit', logger)
    security_audit_role = role_config.get_role()
    audit_role_config = get_aws_data.GetRoles('audit', logger)
    audit_role = audit_role_config.get_role()
    security_role_session_name = "AssumeRoleSecurityAuditSession"
    audit_role_session_name = "AssumeRoleAuditSession"
    access_key = None
    secret_access_key = None
    session_key = None
    audit_cred = get_creds(
        dev_account,
        security_audit_role,
        security_role_session_name,
        access_key,
        secret_access_key,
        session_key,
        logger
    )
    access_key = audit_cred["AccessKeyId"]
    secret_access_key = audit_cred["SecretAccessKey"]
    session_key = audit_cred["SessionToken"]
    sec_audit_cred = get_creds(
        account,
        audit_role,
        audit_role_session_name,
        access_key,
        secret_access_key,
        session_key,
        logger
    )

    return sec_audit_cred


def get_enforce_credentials(account, logger):
    svcs_account_config = get_aws_data.GetAccounts(logger, 'svcs')
    svcs_account = svcs_account_config.get_account()
    role_config = get_aws_data.GetRoles('security_enforce', logger)
    security_enforce_role = role_config.get_role()
    enforce_role_config = get_aws_data.GetRoles('enforce', logger)
    enforce_role = enforce_role_config.get_role()
    security_enforce_role = security_enforce_role
    enforce_role = enforce_role
    security_enforce_role_session_name = "AssumeRoleSecurityEnforceSession"
    enforce_role_session_name = "AssumeRoleEnforceSession"
    access_key = None
    secret_access_key = None
    session_key = None
    sec_enforce_cred = get_creds(
        svcs_account,
        security_enforce_role,
        security_enforce_role_session_name,
        access_key,
        secret_access_key,
        session_key,
        logger
    )
    access_key = sec_enforce_cred["AccessKeyId"]
    secret_access_key = sec_enforce_cred["SecretAccessKey"]
    session_key = sec_enforce_cred["SessionToken"]
    enforce_cred = get_creds(
        account,
        enforce_role,
        enforce_role_session_name,
        access_key,
        secret_access_key,
        session_key,
        logger
    )
    return enforce_cred
