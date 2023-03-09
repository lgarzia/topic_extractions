from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List

from google.cloud import firestore


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

def save_search_results(search_term: str, json_results: Dict[str, Dict]):
    """Expect 

    Args:
        json_results (Dict[str, Dict]): _description_

    TODO: Only Save relevent items of podcasts
    """
    print('in save clause')
    project='podact-topic-extractor'
    db = firestore.Client(project=project)

    user_podcast_ref = []
    podcast_collection = "podcasts"
    podcast_collection_ref = db.collection(podcast_collection)
    for podcast in json_results['results']:
        podcast_document_name = str(podcast['collectionId'])
        podcast_data = Podcast(**{k:v for k,v in podcast.items() if k in Podcast.__match_args__}).__dict__
        podcast_ref = podcast_collection_ref.document(podcast_document_name)
        podcast_ref.set(podcast_data)
        user_podcast_ref.append(podcast_ref)

    search_date = datetime.today().strftime('%Y%m%d')
    search_collection = db.collection("searches")
    search_document_name = f"srch_trm_{str.lower(search_term)}_dte_{search_date}"
    search_result_data = {'search_term': f"{search_term}", 
                        'search_date': f"{search_date}", 
                        'search_result_count': f"{json_results['resultCount']}", 
                        'search_result_podcasts': user_podcast_ref}
    search_ref = search_collection.document(search_document_name)
    search_ref.set(search_result_data)