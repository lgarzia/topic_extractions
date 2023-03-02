import datetime

from flask import Flask, redirect, render_template, request, url_for
from formsical import MyForm
from markupsafe import escape

from flask_bootstrap import Bootstrap5  # isort: skip

app = Flask(__name__)
bootstrap = Bootstrap5(app)


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
    form = MyForm(meta={'csrf': False})
    if form.validate_on_submit():
        print(request.form)
        return redirect('/')
    return render_template('rss_search.html', form=form)

@app.route('/search/<string:search_pod>')
def get_rss_search(search_pod):
    return f"{escape(search_pod)}"

@app.route('/download', methods=['GET', 'POST'])
def get_rss_mp3(search_pod):
    return f"{escape(search_pod)}"

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