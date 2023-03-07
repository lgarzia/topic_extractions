
# gcloud functions describe YOUR_FUNCTION_NAME \
# --gen2 \
# --region=YOUR_FUNCTION_REGION \
# --format="value(serviceConfig.uri)"

import google.auth
import google.auth.transport.requests

creds, project = google.auth.default(scopes=['https://us-central1-podact-topic-extractor.cloudfunctions.net/podcast-search-g1'])
auth_req = google.auth.transport.requests.Request()
creds.refresh(auth_req)

# python -m pytest tests\test_local.py::test_search_itune_search -s
import requests


def test_search_api():
    headers = {'Authorization': f'bearer {creds.id_token}'}
    data={'search_term':'python engineering'}
    url = "https://us-central1-podact-topic-extractor.cloudfunctions.net/podcast-search-g1"
    r = requests.post(url, json=data, headers=headers)
    print(r.json())
    assert r.status_code == 200
