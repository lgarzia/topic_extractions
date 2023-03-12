import feedparser
from feedparser.util import FeedParserDict


def get_rss_download_results(rss_link:str)->FeedParserDict:
    return feedparser.parse(rss_link)