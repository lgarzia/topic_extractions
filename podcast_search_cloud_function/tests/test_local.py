import requests


def test_check():
    assert 1==1


#def test_connection():
#    url = "http://localhost:8080/"
#    r = requests.get(url)
#    assert r.status_code == 200

def test_keyword():
    params={'keyword':'python engineering'}
    url = "http://localhost:8080/"
    r = requests.get(url, params=params)
    assert r.status_code == 200
