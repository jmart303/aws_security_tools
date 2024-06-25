import boto3
import botocore.exceptions


def get_aws_client(service, region, credentials, logger):
    try:
        client = boto3.client(
            service,
            region_name=region,
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken']
        )

        return client
    except botocore.exceptions.ClientError as error:
        logger.critical(f'error establishing guardduty client {error}')
