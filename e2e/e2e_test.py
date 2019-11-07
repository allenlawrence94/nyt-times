import requests
import time
import pytest


url = 'http://172.17.0.1:8080/'


@pytest.fixture(scope='module')
def healthz():
    while requests.get(url + 'healthz').status_code != 200:
        time.sleep(1)
    return


def test_healthz(healthz):
    resp = requests.get(url + 'healthz')
    assert resp.json()['healthy'] == True
