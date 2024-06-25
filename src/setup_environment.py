import logging
import os
import boto3
import botocore.exceptions


class Logger:
    def __init__(self, *args):
        self.start = args[0]
        self.log_file = args[1]

    def conf_logger(self):
        if os.path.isabs(self.log_file):
            os.makedirs(os.path.dirname(self.log_file), exist_ok=True)

        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
            datefmt='%Y-%m-%d %H:%m:%S',
        )
        logger = logging.getLogger()
        logger.info(f'Starting logger {self.start}')
        logging.getLogger('boto3').setLevel(logging.WARNING)
        logging.getLogger('botocore').setLevel(logging.WARNING)

        return logger


def get_aws_enabled_regions(aws_app, srv_credentials):
    enabled_regions = []
    sess = boto3.Session()
    acct_regions = sess.get_available_regions(aws_app)
    for region in acct_regions:
        try:
            regional_sts = boto3.client(
                "sts",
                region_name=region,
                aws_access_key_id=srv_credentials["AccessKeyId"],
                aws_secret_access_key=srv_credentials["SecretAccessKey"],
                aws_session_token=srv_credentials["SessionToken"],
            )
            regional_sts.get_caller_identity()
        except botocore.exceptions.ClientError as boto3_error:
            pass
        else:
            enabled_regions.append(region)
    return enabled_regions
