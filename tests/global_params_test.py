import pytest
from flask import url_for
import faas
import requests
import datetime


destructive_urls = ["/restart", "/stop_listener", "/static"]

@pytest.fixture()
def app():
    faas.require_authentication = False
    app = faas.app
    return app


@pytest.mark.usefixtures('live_server')
@pytest.mark.parametrize("params,expected_delay,expected_response_code", [
    ({"delay": 2, "return_status_code": 222}, 2, 222),
    ({"delay": 2}, 2, 200),
    ({"return_status_code": 404}, 0, 404),
    ({}, 0, 200),
])
def test_server_is_up_and_running(params, expected_delay, expected_response_code):
    endpoints = [url.endpoint for url in app().url_map.iter_rules() if not any([url.rule.startswith(b) for b in destructive_urls])]
    for endpoint in endpoints:
        start = datetime.datetime.now()
        res = requests.get(url_for(endpoint, _external=True, **params))
        end = datetime.datetime.now()
        assert res.status_code == expected_response_code
        assert (end - start).total_seconds() > expected_delay
