import pathlib
import pytest
import httpx
import os
import logging


@pytest.mark.parametrize("username,password,expect_authorization, expect_v1, expect_v2",
                         [("alice", "wonderland", True, True, True),
                          ("bob", "builder", True, True, False),
                          ("clementine", "mandarine", False, False, False)])
def test_authorization(username:str, password:str, expect_authorization, expect_v1, expect_v2):
    assert isinstance(username, str)
    assert isinstance(password, str)
    assert isinstance(expect_authorization, bool)
    assert isinstance(expect_v1, bool)
    assert isinstance(expect_v2, bool)

    address = os.getenv('ADDRESS')
    if address is None:
        address = 'sentiment_analyzer_exam'

    port = os.getenv('PORT')
    if port is None:
        port = 8000
    if not isinstance(port, int):
        try:
            port = int(port)
        except TypeError as e:
            raise e

    will_log = os.getenv('LOG')
    try:
        if isinstance(will_log, str):
            will_log = int(will_log)
        will_log = bool(will_log)
    except (TypeError, ValueError):
        raise Exception('LOG environment variable could not be interpreted as a boolean')

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    if will_log is True:
        log_file_location = pathlib.Path(__file__).parent
        print(log_file_location)
        file_handler = logging.FileHandler(filename=log_file_location / 'api_test.log')
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        logger.addHandler(file_handler)
        logger.info('Started logging')

    permissions_url = f'http://{address}:{port}/permissions'
    login_params = {
        'username': username,
        'password': password
    }
    response = httpx.get(permissions_url, params=login_params)

    can_log_in = (200 <= response.status_code < 300)
    assert can_log_in == expect_authorization
    if expect_authorization is False:
        return

    response_json = response.json()
    actual_permissions = response_json['permissions']

    can_access_v1 = ('v1' in actual_permissions)
    can_access_v2 = ('v2' in actual_permissions)
    assert can_access_v1 == expect_v1
    assert can_access_v2 == expect_v2
