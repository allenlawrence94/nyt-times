import requests
import time
import pytest


url = 'http://172.17.0.1:8080/'


@pytest.fixture(scope='module')
def healthz():
    while True:
        try:
            successful = requests.get(url + 'healthz').status_code == 200
            if successful:
                return
            else:
                time.sleep(1)
        except requests.ConnectionError:
            time.sleep(1)


@pytest.fixture(scope='module')
def users(healthz):
    requests.post(url + 'player', json={"name": "foo"})
    requests.post(url + 'player', json={"name": "bar"})


def test_healthz(healthz):
    resp = requests.get(url + 'healthz')
    assert resp.json()['healthy'] is True


def test_post_time(users):
    assert requests.post(url + 'time', json={
        "player": "foo",
        "time": 22,
        "game": "mini"
    }).status_code == 200
    assert requests.post(url + 'time', json={
        "player": "foo",
        "time": 18,
        "game": "mini"
    }).status_code == 422


def test_get_players(users):
    resp = requests.get(url + 'players')
    assert resp.status_code == 200
    assert resp.json() == ['foo', 'bar']


def test_get_winner(users):
    requests.post(url + 'time', json={
        "player": "foo",
        "time": 22,
        "game": "mini"
    })
    requests.post(url + 'time', json={
        "player": "bar",
        "time": 18,
        "game": "mini"
    })
    resp = requests.get(url + 'winner', params={'game': 'mini'})
    assert resp.status_code == 200
    assert resp.json()[0]["player"] == "bar"
    assert len(resp.json()) == 1
