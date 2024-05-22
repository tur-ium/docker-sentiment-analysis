import pathlib
import pytest
import httpx
import os
import logging


@pytest.mark.parametrize("username,password,expect_authentication",
                         [("alice", "wonderland", True),
                          ("bob", "builder", True),
                          ("clementine", "mandarine", False)])
def test_authentication(username:str, password:str, expect_authentication):
    assert isinstance(username, str)
    assert isinstance(password, str)
    assert isinstance(expect_authentication, bool)

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
    logger.info(response.status_code)
    logger.info(response.text)
    print('Done')
    can_log_in = (200 <= response.status_code < 300)
    assert can_log_in == expect_authentication
