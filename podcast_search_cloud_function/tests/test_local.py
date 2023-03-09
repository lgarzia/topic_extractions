import requests


def test_keyword_query_string():
    params={'search_term':'python engineering'}
    url = "http://localhost:8080/"
    r = requests.get(url, params=params)
    print(r.json())
    assert r.status_code == 400

def test_keyword_query_string_fail_no_search_term():
    params={'search_terms':'python engineering'}
    url = "http://localhost:8080/"
    r = requests.get(url, params=params)
    print(r.json())
    assert r.status_code == 200

def test_keyword_post_json():
    data={'search_term':'python engineering'}
    url = "http://localhost:8080/"
    r = requests.post(url, json=data)
    print(r.json())
    assert r.status_code == 200
#https://cloud.google.com/functions/docs/samples/functions-http-content

def test_keyword_post_form():
    data={'search_term':'python engineering'}
    url = "http://localhost:8080/"
    r = requests.post(url, data=data)
    print(r.json())
    assert r.status_code == 200

def test_return_json():
    data={'keyword':'python engineering'}
    url = "http://localhost:8080/"
    r = requests.post(url, json=data)
    print(r.json())
    assert r.status_code == 200

def test_error_method():
    data={'keyword':'python engineering'}
    url = "http://localhost:8080/"
    r = requests.put(url, params=data)
    print(r.json())
    assert r.status_code == 400

# python -m pytest tests\test_local.py::test_search_itune_search -s
def test_search_itune_search():
    from search import itune_podcast_search
    r = itune_podcast_search('python')
    print(r.json())
    assert r.status_code == 200

# python -m pytest tests\test_local.py::test_search_itune_search -s
def test_search_api():
    data={'search_term':'python engineering'}
    url = "http://localhost:8080/"
    r = requests.post(url, json=data)
    print(r.json())
    assert r.status_code == 200

# python -m pytest tests\test_local.py::test_search_datastore_save_api -s
def test_search_datastore_save_api():
    data={'search_term':'python', 'save':True}
    url = "http://localhost:8080/"
    r = requests.post(url, json=data)
    print(r.json())
    assert r.status_code == 200