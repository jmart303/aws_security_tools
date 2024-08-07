import botocore.exceptions
import botocore.errorfactory
import multiprocessing
import get_aws_data
import get_aws_service_client
import setup_environment
import pull_aws_accounts
import credentials
from datetime import datetime


def pull_public_ips(account, region, logger, next_token):
    public_ip_details = {
        'public_ip': None,
        'owner': None,
        'dns_name': None,
    }
    enforce_credentials = credentials.get_enforce_credentials(account, logger)
    client = get_aws_service_client.get_aws_client('ec2', region, enforce_credentials, logger)
    try:
        ec2_network_interfaces = client.describe_network_interfaces(
            NextToken=next_token,
            MaxResults=50
        )
        if len(ec2_network_interfaces["NetworkInterfaces"]) > 0:
            for eni in ec2_network_interfaces["NetworkInterfaces"]:
                if "Association" in eni:
                    public_ip = eni["Association"].get("PublicIp")
                    ip_owner_id = eni["Association"].get("IpOwnerId")
                    public_dns_name = eni["Association"].get("PublicDnsName")
                    instance_owner_id = eni["Association"].get('InstanceOwnerId')
                    public_ip_details = {
                        'account': account,
                        'region': region,
                        'public_ip': public_ip,
                        'owner_id': ip_owner_id,
                        'dns_name': public_dns_name,
                        'instance_owner_id': instance_owner_id
                    }
                    return public_ip_details
        else:
            return public_ip_details
    except botocore.exceptions.ClientError as error:
        logger.critical(f'error getting network interfaces in account {account} {error}')


def main(account, region, logger):
    next_token_check = True
    first_run = 0
    next_token = ''
    try:
        while next_token_check:
            if first_run == 0:
                response = pull_public_ips(account, region, logger, next_token)
                next_token = response['NextToken']
                print(f'LOOK {response}')
            else:
                if next_token:
                    response = pull_public_ips(account, region, logger, next_token)
                    next_token = response['NextToken']
                    print(f'LOOK AGAIN {response}')
                else:
                    next_token_check = False

    except botocore.errorfactory.ClientError as e:
        logger.critical(f'error listing network interface details {e}')


if __name__ == '__main__':
    start = datetime.now()
    log_file = f'./logs/public_ip.log'
    logger_config = setup_environment.Logger(start, log_file)
    logger = logger_config.conf_logger()
    account_config = get_aws_data.GetAccounts(logger, 'master')
    master_account = account_config.get_account()

    audit_credentials = credentials.get_audit_credentials(master_account, logger)
    regions = setup_environment.get_aws_enabled_regions('ec2', audit_credentials)

    target_accounts = pull_aws_accounts.list_accounts(audit_credentials, logger)
    with open('dev_accounts.txt', 'a') as file:
        for account in target_accounts:
            file.write(f'{account}\n')

    # job_arguments = [[account, region, logger]
    #                  for account in target_accounts
    #                  for region in regions
    #                  ]
    # with multiprocessing.Pool(processes=10)as pool:
    #     pool.starmap(main, job_arguments)
