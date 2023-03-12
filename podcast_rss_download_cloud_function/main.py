"""Cloud Function that accepts search term and returns results from Apple itune API 

A simple wrapper around Apple API searching for podcast media

Usage Example:
  request.get(url/<search term>)

"""
import functions_framework
from data_model import save_rss_download_results
from flask import jsonify
from google.cloud import firestore
from rss_download import get_rss_download_results


# Register an HTTP function with the Functions Framework
# https://tedboy.github.io/flask/generated/generated/flask.Request.html
#https://flask.palletsprojects.com/en/2.1.x/quickstart/#about-responses
@functions_framework.http
def podcast_rss_download(request):
  """ """
  collectionId = None
  # part one - collect search_term
  if request.method == 'GET':
    collectionId = request.args.get('collectionId')
  elif request.method == 'POST':
    if request.is_json:
      collectionId = request.json.get('collectionId')
    elif request.content_type == 'application/x-www-form-urlencoded':
        collectionId = request.form.get('collectionId')
    else:
        collectionId= request.data.get('collectionId')
  else:
    return jsonify({'error_message':'only support GET/POST'}), 400

  if collectionId:
        # retrieve rss feed
        project='podact-topic-extractor'
        db = firestore.Client(project=project)
        podcasts_collection = 'podcasts'
        podcasts_collection_ref = db.collection(podcasts_collection)
        podcasts_collection_document = podcasts_collection_ref.document(collectionId).get().to_dict()
        if podcasts_collection_document:
            # download rss feed and save
            print(f"collection id provided - {collectionId}")
            rss_link = podcasts_collection_document['feedUrl']
            print(f"rss link found = {rss_link}")
            rss_results = get_rss_download_results(rss_link)
            if rss_results['bozo']==0: # well-formed
                if request.json.get('save'):
                    save_rss_download_results(collectionId, rss_results) 
                    return rss_results
                else:
                     return rss_results
            else:
                return jsonify({'error_message':'invalid rss feed'}), 400                                
        else:
            return jsonify({'error_message':'please provide collectionId'}), 400            
        
  else:
     return jsonify({'error_message':'please provide collectionId'}), 400