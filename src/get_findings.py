import botocore.exceptions
import botocore.errorfactory
import get_aws_service_client
import get_aws_data
import credentials
import get_detector_id
import setup_environment
import json
from datetime import datetime


def describe_findings(detector, finding_id, count):
    try:
        response = client.get_findings(
            DetectorId=detector,
            FindingIds=[
                finding_id,
            ],
        )
        try:
            finding_severity = response['Findings'][0]['Severity']
            access_details = ''
            instance_details = ''
            resource_type = ''
            if finding_severity >= 7:
                severity = 'high'
                account = response['Findings'][0]['AccountId']
                finding_region = response['Findings'][0]['Region']
                description = response['Findings'][0]['Description']
                try:
                    access_details = response['Findings'][0]['Resource']['AccessKeyDetails']
                except KeyError as e:
                    logger.info(f'no access key details found {e}')
                try:
                    instance_details = response['Findings'][0]['Resource']['InstanceDetails']
                except KeyError as e:
                    logger.info(f'no instance details found {e}')
                try:
                    resource_type = response['Findings'][0]['Resource']['ResourceType']
                except KeyError as e:
                    logger.info(f'no resource type found {e}')

                service_action = response['Findings'][0]['Service']['Action']
                service_count = response['Findings'][0]['Service']['Count']
                title = response['Findings'][0]['Title']
                finding_type = response['Findings'][0]['Type']

                findings_dict = {
                    'severity': severity,
                    'account': account,
                    'finding region': finding_region,
                    'description': description,
                    'action': service_action,
                    'occurrences': service_count,
                    'title': title,
                    'type': finding_type,
                    'access_details': access_details,
                    'instance_details': instance_details,
                    'resource_type': resource_type

                }
                output = json.dumps(findings_dict, indent=4)
                print(f'{output}')
            else:
                print(f'details {detector} {region} {finding_id} {count}')
        except KeyError as e:
            logger.info(f'missing keys for findings {e}')
    except botocore.exceptions.ClientError as e:
        logger.critical(f'error describing findings {e}')


def list_findings(detector, next_token):
    try:
        response = client.list_findings(
            DetectorId=detector,
            FindingCriteria={
                'Criterion': {
                    'severity': {
                        'Eq': [
                            '7', '8', '9'
                        ],
                    }
                }
            },
            MaxResults=25,
            NextToken=next_token
        )
        return response
    except botocore.exceptions.ClientError as e:
        logger.critical(f'error listing high findings {e}')


def get_findings(detector):
    count = 0
    next_token_check = True
    first_run = 0
    next_token = ''
    try:
        while next_token_check:
            if first_run == 0:
                response = list_findings(detector, next_token)
                results = response['FindingIds']
                next_token = response['NextToken']
                for finding in results:
                    count += 1
                    describe_findings(detector, finding, count)
                first_run += 1
            else:
                if next_token:
                    response = list_findings(detector, next_token)
                    results = response['FindingIds']
                    next_token = response['NextToken']
                    for finding in results:
                        count += 1
                        describe_findings(detector, finding, count)

                else:
                    next_token_check = False

    except botocore.errorfactory.ClientError as e:
        logger.critical(f'error listing guardduty findings {e}')


def list_detector_ids():
    try:
        response = client.list_detectors(
            MaxResults=50
        )
        detector = response['DetectorIds']
        return detector[0]
    except botocore.exceptions.ClientError as e:
        logger.critical(f'error retrieving detector id {e}')


if __name__ == '__main__':
    start = datetime.now()
    log_file = f'./logs/gdf.log'
    logger_config = setup_environment.Logger(start, log_file)
    logger = logger_config.conf_logger()

    account_config = get_aws_data.GetAccounts(logger, 'gd')
    gd_account = account_config.get_account()
    audit_credentials = credentials.get_audit_credentials(gd_account, logger)

    regions = setup_environment.get_aws_enabled_regions('ec2', audit_credentials)
    if regions:
        for region in regions:
            client = get_aws_service_client.get_aws_client('guardduty', region, audit_credentials, logger)
            detector_id = get_detector_id.list_detector_ids(client, logger)
            try:
                get_findings(detector_id)
            except botocore.exceptions.ParamValidationError as error:
                logger.error(f'no detector id for {region}')
        end = datetime.now()
        logger.info(f'Finished run {end}')
    else:
        end = datetime.now()
        logger.critical(f'no enabled regions configured. Finished {end}')
