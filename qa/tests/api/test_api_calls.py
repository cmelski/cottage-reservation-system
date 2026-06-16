import os
import pytest
from qa.core.utils.logging_utils import get_logger
from qa.business_logic.api.cottage_api import CottageAPI


logger = get_logger(__name__)

@pytest.mark.smoke
@pytest.mark.api_cottage
def test_api_cottage(reset_db, api_client):
    cottage_api = CottageAPI(api_client)
    cottage_api_response = cottage_api.get_cottage()
    response_status = cottage_api_response.status_code
    assert response_status == 200
    logger.info(cottage_api_response.json())
