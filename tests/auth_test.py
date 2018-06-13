import pytest
from flask import url_for
import faas
import requests
import datetime

secret_token = "secret_token_123"

@pytest.fixture()
def app():
    faas.require_authentication = True
    faas.application_tokens = [secret_token]
    app = faas.app
    return app


@pytest.mark.usefixtures('live_server')
class TestLiveServerGlobalParams(object):

    @pytest.mark.parametrize("endpoint,params,response_code", [
        ('index', [], 401),
        ('logs', [], 401),
        ('oom', [], 401),
        ('restart', [], 401),
        ('stop_listener', [], 401),
        ('ping', [], 200),
    ])
    def test_server_is_up_and_running(self, endpoint, params, response_code):
        res = requests.get(url_for(endpoint, _external=True, *params))
        assert res.status_code == response_code

    def test_delay(self):
        res = requests.get(url_for('logs', _external=True))
        assert res.status_code == 401

    def test_status_code(self):
        start = datetime.datetime.now()
        res = requests.get(url_for('index', delay=3, return_status_code=222, _external=True))
        stop = datetime.datetime.now()
        assert 'Invalid application_token' in res.text
        assert res.status_code == 401
        assert (stop - start).total_seconds() > 3

    def test_valid_token(self):
        res = requests.get(url_for('index', application_token=secret_token, _external=True))
        assert res.status_code == 200
