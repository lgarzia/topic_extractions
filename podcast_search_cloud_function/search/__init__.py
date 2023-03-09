import data_model
import requests


def itune_podcast_search(search_term: str, limit:int=10, save=False):
    country = "us"
    limit = 10
    base_url = "https://itunes.apple.com"
    search_url = f"{base_url}/search"
    params = {"term": search_term, "country": country, "limit": limit, "media": "podcast"}
    response = requests.get(url=search_url, params=params)
    if save:
        print('in save')
        data_model.save_search_results(search_term, response.json())
    return response