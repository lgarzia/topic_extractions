# %%
import podsearch

# %%
podcasts = podsearch.search("python", country="us", limit=10)

# %%
from podsearch import http

# %%
# Trying to look at raw results
# https://developer.apple.com/library/archive/documentation/AudioVideo/Conceptual/iTuneSearchAPI/UnderstandingSearchResults.html#//apple_ref/doc/uid/TP40017632-CH8-SW1
query = "python"
country = "us"
limit = 10
BASE_URL = "https://itunes.apple.com"
SEARCH_URL = f"{BASE_URL}/search"
params = {"term": query, "country": country, "limit": limit, "media": "podcast"}
response = http.get(url=SEARCH_URL, params=params)
# %%

response # dict
# %%
response.keys() # dict_keys(['resultCount', 'results'])

# returns list
r = response['results'][0]
# %%
# dict_keys(['wrapperType', 'kind', 'collectionId', 'trackId', 'artistName', 'collectionName', 'trackName', 'collectionCensoredName', 'trackCensoredName', 'collectionViewUrl', 'feedUrl', 'trackViewUrl', 'artworkUrl30', 'artworkUrl60', 'artworkUrl100', 'collectionPrice', 'trackPrice', 'collectionHdPrice', 'releaseDate', 'collectionExplicitness', 'trackExplicitness', 'trackCount', 'trackTimeMillis', 'country', 'currency', 'primaryGenreName', 'contentAdvisoryRating', 'artworkUrl600', 'genreIds', 'genres'])
# %%
# jackpot -> hase a 'releaseDate'
y = [(p['collectionName'], p['releaseDate']) for p in response['results']]
# %%

y
# %%
from datetime import datetime

datetime_str = '2016-10-01T03:00:00Z'
datetime_object = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%SZ')
# %%
