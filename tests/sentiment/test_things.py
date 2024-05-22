import pathlib
import pytest
import httpx
import os
import logging


@pytest.mark.parametrize("username,password,sentence,expect_v1,expect_v2,expect_positive",
                         [
                             ("alice", "wonderland", "life is beautiful", True, True, True),
                             ("bob", "builder", "life is beautiful", True, False, True),
                             ("clementine", "mandarine", "life is beautiful", False, False, True),
                             ("alice", "wonderland", "that sucks", True, True, False),
                             ("bob", "builder", "that sucks", True, False, False),
                             ("clementine", "mandarine", "that sucks", False, False, False)
                         ])
def test_sentiment(username: str, password: str, sentence, expect_v1: bool, expect_v2: bool, expect_positive: bool):
    assert isinstance(username, str)
    assert isinstance(password, str)
    assert isinstance(sentence, str)
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

    sentiment_url_v1 = f'http://{address}:{port}/v1/sentiment'
    login_params = {
        'username': username,
        'password': password,
        'sentence': sentence
    }
    send_and_check_sentiment(logger=logger, sentiment_url=sentiment_url_v1, login_params=login_params,
                             expect_authorization=expect_v1, expect_positive=expect_positive)

    sentiment_url_v2 = f'http://{address}:{port}/v2/sentiment'
    send_and_check_sentiment(logger=logger, sentiment_url=sentiment_url_v2, login_params=login_params,
                             expect_authorization=expect_v2, expect_positive=expect_positive)


def send_and_check_sentiment(logger: logging.Logger, sentiment_url: str, login_params: dict, expect_authorization,
                             expect_positive: bool):
    response = httpx.get(sentiment_url, params=login_params)

    logger.info(response.status_code)
    if expect_authorization and not (200 <= response.status_code < 300):
        raise Exception("Not able to get score with v1")
    if expect_authorization is False:
        assert 400 <= response.status_code < 500
        return

    logger.info(response.json())

    response_json = response.json()
    score = response_json['score']
    if expect_positive:
        assert score > 0
    else:
        assert score < 0
