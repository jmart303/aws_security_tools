import get_aws_service_client
import credentials
import setup_environment
import get_aws_data
import list_ou_accounts
import json

from datetime import datetime


def list_org():
    client = get_aws_service_client.get_aws_client('organizations', 'us-east-1', audit_credentials,
                                                   logger)

    response = client.list_organizational_units_for_parent(
        ParentId=parent_id
    )
    for ou in response['OrganizationalUnits']:
        ou_name = ou['Name']
        ou_id = ou['Id']
        try:
            account, name, status = list_ou_accounts.list_ou_accounts(ou_id, logger, audit_credentials)
            print(f'{ou_name} {account} {name} {status}')
        except TypeError as e:
            logger.critical(f'error accessing ou details {e}')


if __name__ == '__main__':
    start = datetime.now()
    log_file = f'./logs/list_org.log'
    logger_config = setup_environment.Logger(start, log_file)
    logger = logger_config.conf_logger()
    account_config = get_aws_data.GetAccounts(logger, 'master')
    master_account = account_config.get_account()
    # audit_credentials = credentials.get_audit_credentials(master_account, logger)
    """
    import private json file of parent ous
    """
    with open('private/parent_ous.json', 'r') as file:
        data = json.load(file)
        parent_id = data['dev_master']['parent_id']
        dev_master_account = data['dev_master']['account']
        audit_credentials = credentials.get_audit_credentials(dev_master_account, logger)
        list_org()
