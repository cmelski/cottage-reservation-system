import pytest
import os
from qa.utils.logging_utils import get_logger
from qa.api.api_client import APIClient

logger = get_logger(__name__)


def test_api_calls(reset_db, api_config_loader):
    api_client = APIClient(os.environ.get('BASE_URL'))
    logger.info(api_config_loader['endpoints'])
    for endpoint in api_config_loader['endpoints']:
        url = endpoint['url']
        method = endpoint['method']
        expected_status = endpoint['expected_status']
        response = api_client.call_api_with_retry(url, method)
        response_status = response.status_code
        assert expected_status == response_status
        logger.info(response.json())
