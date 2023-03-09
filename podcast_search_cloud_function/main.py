"""Cloud Function that accepts search term and returns results from Apple itune API 

A simple wrapper around Apple API searching for podcast media

Usage Example:
  request.get(url/<search term>)

"""
import functions_framework
from flask import jsonify
from search import itune_podcast_search

# from localpackage import hello_local_package


# Register an HTTP function with the Functions Framework
# https://tedboy.github.io/flask/generated/generated/flask.Request.html
#https://flask.palletsprojects.com/en/2.1.x/quickstart/#about-responses
@functions_framework.http
def podcast_search(request):
  """ """
  search_term = None
  # part one - collect search_term
  if request.method == 'GET':
    search_term = request.args.get('search_term')
  elif request.method == 'POST':
    if request.is_json:
      search_term = request.json.get('search_term')
    elif request.content_type == 'application/x-www-form-urlencoded':
        search_term = request.form.get('search_term')
    else:
        search_term = request.data.get('search_term')
  else:
    return jsonify({'error_message':'only support GET/POST'}), 400

  if search_term:
        response = itune_podcast_search(search_term, save=request.json.get('save')) 
        return response.json(), response.status_code
  else:
     return jsonify({'error_message':'please provide search_term'}), 400