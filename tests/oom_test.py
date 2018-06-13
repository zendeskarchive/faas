import pytest
from flask import url_for
import faas
import requests
import datetime
import os
import psutil
import sys


@pytest.fixture()
def app():
    faas.require_authentication = False
    app = faas.app
    return app



@pytest.mark.usefixtures('live_server')
class TestLiveServerGlobalParams(object):


    def _get_mem_info(self):
        res = requests.get(url_for('info', _external=True))
        return res.json()['memory']['rss'] / 1024 ** 2

    @pytest.mark.parametrize("params,expected_response_code", [
        ({"memory_mb_to_allocate": 50, "steps": 1, "sleep_between_steps": 0}, 200),
        ({"memory_mb_to_allocate": 50, "steps": 3, "sleep_between_steps": 3}, 200),
    ])
    def test_oom(self, params, expected_response_code):
        mem_before = self._get_mem_info()
        start = datetime.datetime.now()
        res = requests.get(url_for('oom', _external=True, **params))
        end = datetime.datetime.now()
        mem_after = self._get_mem_info()
        assert (mem_after - mem_before) >= (params.get('memory_mb_to_allocate') / params.get('steps'))
        assert res.status_code == 200
        assert (end - start).total_seconds() > params.get('sleep_between_steps', 0) * params.get('steps')
        assert "MB in step {}".format(params.get('steps') - 1) in res.text
