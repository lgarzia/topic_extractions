# %%
import podsearch

# %%
podcasts = podsearch.search("Google Cloud Reader", country="us", limit=10)

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
results = response['results'][1]
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
# working out the firestore logic
# collection for search 
# collection for podcasts
# https://firebase.google.com/docs/firestore/manage-data/structure-data
# %%
# do manually first 

# parse responses
# work out edge cases
# add to cloud function
# work out user/machine logic from Flask

# %%
from google.cloud import firestore

# %%
project='podact-topic-extractor'
db = firestore.Client(project=project)
# %%
# idea - create podcast - get reference and store
podcast_collection = "podcasts"
podcast_document_name = '1214664324'  # 'collectionId' 
podcast_ref = db.collection(podcast_collection).document(podcast_document_name)
podcast_document_data = {'collectionId': 1214664324, 
                         'artistName': 'Dr. Charles Russell Severance'}
podcast_ref.set(podcast_document_data)
# %%
search_collection = "searches"
search_term = "python"
search_date = "20230309"
search_document_name = f"src_trm_{str.lower(search_term)}_dte_{search_date}"
search_result_data = {'search_term': f"{search_term}", 
                      'search_date': f"{search_date}", 
                      'search_result_count': f"{3}", 
                      'search_result_podcasts': [podcast_ref]}
# %%
search_ref = db.collection(search_collection).document(search_document_name)
# %%
search_ref.set(search_result_data)

# %%
# retrieve all whole document
get_search_doc = db.collection(search_collection).document(search_document_name).get()

# %%
podcast_list = search_ref.get('search_result_podcasts')
# %%
get_search_doc.get('search_date')

# %%
s = get_search_doc.get('search_result_podcasts')
# %%
for i in s:
    print(i.get().to_dict())
# %%
get_search_doc.to_dict()
# %%
# create function to process data
# note --> this returns just dictionary; leveraging request need to pull out json
response = http.get(url=SEARCH_URL, params=params)

# %%
podcast_results = response['results'][1]

# %%
user_podcast_ref = []
podcast_collection = "podcasts"
podcast_collection_ref = db.collection(podcast_collection)
for podcast in response['results']:
    podcast_document_name = str(podcast['collectionId'])
    podcast_data = podcast
    podcast_ref = podcast_collection_ref.document(podcast_document_name)
    podcast_ref.set(podcast_data)
    user_podcast_ref.append(podcast_ref)
    print(podcast_document_name)
# %%
from datetime import datetime

print()
# %%
search_term = "python"
search_date = datetime.today().strftime('%Y%m%d')
search_document_name = f"srch_trm_{str.lower(search_term)}_dte_{search_date}"
search_result_data = {'search_term': f"{search_term}", 
                      'search_date': f"{search_date}", 
                      'search_result_count': f"{response['resultCount']}", 
                      'search_result_podcasts': user_podcast_ref}
# %%
search_ref = db.collection(search_collection).document(search_document_name)
# %%
search_ref.set(search_result_data)
# %%
# search_ref = db.collection(search_collection).document("src_trm_python_dte_datetime.today().strftime('%Y%m%d')").delete()
# search_ref = db.collection(search_collection).document("src_trm_python_dte_20230309").delete()
# %%
from dataclasses import dataclass
from typing import List


@dataclass
class Podcast:
    artistName: str
    collectionId: str
    collectionName: str
    collectionViewUrl: str
    feedUrl: str
    genres: List[str]
    primaryGenreName: str
    releaseDate: datetime

# %%
p = Podcast(**{k:v for k,v in podcast_data.items() if k in Podcast.__match_args__})
# %%
p.to_dict()
#c = Config(**{k:v for k,v in os.environ.items() if k in field_names})
# %%
