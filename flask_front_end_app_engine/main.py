import datetime
import os

import requests
from data_model import rehydrate_search
from flask import Flask, redirect, render_template, request, url_for
from formsical import PodcastSearchForm, RSSDownloadForm
from google.cloud import firestore
from markupsafe import escape

from flask_bootstrap import Bootstrap5  # isort: skip

app = Flask(__name__)
bootstrap = Bootstrap5(app)

# https://stackoverflow.com/questions/63634151/how-can-i-call-a-google-cloud-function-from-google-app-engine
def get_access_token_headers():
    if os.getenv('GAE_ENV', '').startswith('standard'):
  # Production in the standard environment
        token_response = requests.get('http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/identity?audience=' +
        'https://us-central1-podact-topic-extractor.cloudfunctions.net/podcast-search-g1', 
        headers={'Metadata-Flavor': 'Google'})
        headers = {'Authorization': f"Bearer {token_response.content.decode('utf-8')}"}
        return headers
    else:
        import google.auth
        import google.auth.transport.requests
        creds, project = google.auth.default(scopes=['https://us-central1-podact-topic-extractor.cloudfunctions.net/podcast-search-g1'])
        auth_req = google.auth.transport.requests.Request()
        creds.refresh(auth_req)
        headers = {'Authorization': f'bearer {creds.id_token}'}
        return headers
  # Local execution.
    
@app.route('/', methods=['GET', 'POST'])
def index():
    error = {}
    dummy_podcasts = ["podcast1","podcast2","podcast3"]
    print(request.method, request.host_url)
    print(request.form)
    app.logger.debug('test logger')
    return render_template('index.html', podcasts=dummy_podcasts)


@app.route('/rss_search', methods=['GET', 'POST'])
def rss_search():
    form = PodcastSearchForm(meta={'csrf': False})
    if form.validate_on_submit():
        # call data model 
        print(f"in form validation - {request.form}")
        # Add logic here to take keyword
        search_res = rehydrate_search("python")
        if search_res:
            print(f"returning from firestore - {search_res}")
            podcasts = search_res['search_result_podcasts']
        #data={'search_term':'python engineering'}
        #url = f"https://us-central1-podact-topic-extractor.cloudfunctions.net/podcast-search-g1"
        #headers = get_access_token_headers()
        #r = requests.post(url, json=data, headers=headers)
        #print(r.json())
        return render_template('rss_search.html', form=form, podcasts=podcasts)
    return render_template('rss_search.html', form=form)


@app.route('/rss_download', methods=['GET', 'POST'])
@app.route('/rss_download/<string:podcast_id>')
def rss_download(podcast_id=None):
    form = RSSDownloadForm(meta={'csrf': False})
    if podcast_id:
        return render_template('rss_download.html', form=form, podcast_id=podcast_id)
    else:
        return render_template('rss_download.html', form=form)


@app.get('/results')
def get_results():
    return f"Here's the results"

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    print('in main')
    app.run(host='127.0.0.1', port=8080, debug=True)