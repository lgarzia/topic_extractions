from typing import Dict, Optional

from google.cloud import firestore


def rehydrate_search(search_term: str) -> Optional[Dict]:
        project='podact-topic-extractor'
        db = firestore.Client(project=project)
        search_date = "20230309" #datetime.today().strftime('%Y%m%d')
        search_collection = db.collection("searches")
        search_document_name = f"srch_trm_{str.lower(search_term)}_dte_{search_date}"
        search_res = search_collection.document(search_document_name).get().to_dict()
        if search_res:
            podcast_ref_hyrd = []
            for podcast_ref in search_res['search_result_podcasts']:
                podcast_ref_hyrd.append(podcast_ref.get().to_dict())
            search_res['search_result_podcasts'] = podcast_ref_hyrd
            return search_res
        else:
            return None
            