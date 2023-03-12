from feedparser.util import FeedParserDict
from google.cloud import firestore


def save_rss_download_results(collectionId: str, feedparser_results: FeedParserDict, limit: int=10):
    print(f"in save rss download - {collectionId}")
    project='podact-topic-extractor'
    db = firestore.Client(project=project)
    podcasts_rss_feed_collection = 'podcasts_rss_feed'
    podcasts_rss_feed_collection_ref = db.collection(podcasts_rss_feed_collection)
    podcasts_rss_feed_document_ref = podcasts_rss_feed_collection_ref.document(collectionId)
    podcasts_rss_feed_entries_collection = "podcasts_rss_feed_entries"
    podcasts_rss_feed_document_entries_collection_ref = podcasts_rss_feed_document_ref.collection(podcasts_rss_feed_entries_collection)
    # create root level document
    podcasts_rss_feed = {}
    podcasts_rss_feed['collectionId'] = collectionId
    podcasts_rss_feed['feed'] = feedparser_results['feed']
    podcasts_rss_feed['href'] = feedparser_results['href']
    podcasts_rss_feed['rss_verions'] = feedparser_results['version']
    # create link subcollection documents
    podcasts_rss_feed['entries'] = [podcasts_rss_feed_document_entries_collection_ref.document(i['id']) for i in feedparser_results['entries'][0:limit]]
    podcasts_rss_feed_document_ref.set(podcasts_rss_feed)
    # create subcollection documents
    for field in feedparser_results['entries'][0:limit]:
        podcasts_rss_feed_entries = {}
        podcasts_rss_feed_entries['id'] = field['id']
        podcasts_rss_feed_entries['collectionid'] = collectionId
        podcasts_rss_feed_entries['raw_field'] = field 
        podcasts_rss_feed_entries['audio_link'] = [f for f in field['links'] if f['type'] in ('audio/mpeg')][0]
        podcasts_rss_feed_document_entries_collection_ref.document(podcasts_rss_feed_entries['id']).set(podcasts_rss_feed_entries)