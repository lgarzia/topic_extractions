"""
A sample Hello World server.
"""
import os

from flask import Flask, jsonify, render_template, request

# pylint: disable=C0103
app = Flask(__name__)

#@app.route('/', methods=['GET', 'POST'])
##def default():
#    return 'yes'

@app.route('/', methods=['GET', 'POST'])
def download_mp3():
    """Return a friendly HTTP greeting."""
    print('hit')
    collectionid = None
    episodeid = None
    mp3url = None  # TODO can query FireStore to 

    # part one - collect search_term
    if request.method == 'GET':
        collectionid = request.args.get('collectionid')
        episodeid = request.args.get('episodeid')
        mp3url = request.args.get('mp3url')

    elif request.method == 'POST':
        if request.is_json:
            collectionid = request.json.get('collectionid')
            episodeid = request.json.get('episodeid')
            mp3url = request.json.get('mp3url')

        elif request.content_type == 'application/x-www-form-urlencoded':
            collectionid = request.form.get('collectionid')
            episodeid = request.form.get('episodeid')
            mp3url = request.form.get('mp3url')
        else:
            collectionid = request.data.get('collectionid')
            episodeid = request.data.get('episodeid')
            mp3url = request.data.get('mp3url')
    else:
        return jsonify({'error_message':'only support GET/POST'}), 400

    if all([collectionid, episodeid, mp3url]):
        response = {'collectionid': collectionid, 
                    'episodeid': episodeid, 
                    'mp3url': mp3url} 
        return jsonify(response)
    else:
        return jsonify({'error_message':'please provide appropriate keys'}), 400

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')
