import datetime

from flask import Flask, render_template
from markupsafe import escape

app = Flask(__name__)


@app.route('/')
def root():
    error = {}
    dummy_times = [datetime.datetime(2018, 1, 1, 10, 0, 0),
                   datetime.datetime(2018, 1, 2, 10, 30, 0),
                   datetime.datetime(2018, 1, 3, 11, 0, 0),
                   ]

    return render_template('index.html', times=dummy_times)

@app.route('/search')
def rss_search():
    return f"{escape('in search forms')}"

@app.route('/search/<string:search_pod>')
def get_rss_search(search_pod):
    return f"{escape(search_pod)}"


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