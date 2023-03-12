import requests


# python -m pytest tests\test_local.py::test_save_rss_download_results -s
def test_save_rss_download_results_local_direct():
    import feedparser
    from data_model import save_rss_download_results
    rss_link = "https://talkpython.fm/episodes/rss"
    collectionId = "979020229"
    # get rss_feed
    feedparser_results = feedparser.parse(rss_link)
    if feedparser_results['bozo'] == 0 : #<-- well-formed
        save_rss_download_results(collectionId, feedparser_results)
    assert True == True

# python -m pytest tests\test_local.py::test_rss_search_datastore_no_save_api -s
def test_rss_search_datastore_no_save_api():
    data={'collectionId':'979020229', 'save':False}
    url = "http://localhost:8080/"
    r = requests.post(url, json=data)
    print(r.json())
    assert r.status_code == 200

# python -m pytest tests\test_local.py::test_rss_search_datastore_save_api -s
def test_rss_search_datastore_save_api():
    data={'collectionId':'890348705', 'save':True}
    url = "http://localhost:8080/"
    r = requests.post(url, json=data)
    print(r.json())
    assert r.status_code == 200