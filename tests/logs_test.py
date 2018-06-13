import pytest
from flask import url_for
import faas
import requests
import datetime
import os


@pytest.fixture()
def app(tmpdir_factory):
    tmp_dir = tmpdir_factory.mktemp("log")
    faas.require_authentication = False
    faas.log_directory = tmp_dir.realpath()
    app = faas.app
    return app


@pytest.mark.usefixtures('live_server')
@pytest.mark.parametrize("params,expected_response_code", [
    ({"bytes_per_second": 1024**2, "seconds": 1, "output_fd": 'testlog'}, 200),
    ({"bytes_per_second": 1024**2, "seconds": 1, "output_fd": '/tmp/testlog2'}, 200),
])
def test_generating_file(tmpdir_factory, app, params, expected_response_code):
    start = datetime.datetime.now()
    res = requests.get(url_for('logs', _external=True, **params))
    end = datetime.datetime.now()
    assert res.status_code == expected_response_code
    assert (end - start).total_seconds() > params.get('seconds', 1)
    assert os.path.getsize(os.path.join(str(faas.log_directory), os.path.basename(params.get('output_fd')))) >= params.get('bytes_per_second')
