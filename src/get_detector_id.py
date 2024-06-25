import botocore.exceptions


def list_detector_ids(client, logger):
    try:
        response = client.list_detectors(
            MaxResults=50
        )
        detector = response['DetectorIds']
        return detector[0]
    except botocore.exceptions.ClientError as error:
        logger.critical(f'error listing detectors {error}')
    except IndexError as error:
        logger.critical(f'error listing detector {error}')