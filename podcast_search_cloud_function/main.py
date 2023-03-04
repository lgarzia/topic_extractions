"""Cloud Function that accepts search term and returns results from Apple itune API 

A simple wrapper around Apple API searching for podcast media

Usage Example:
  request.get(url/<search term>)

"""
import functions_framework

# from localpackage import hello_local_package


# Register an HTTP function with the Functions Framework
# https://tedboy.github.io/flask/generated/generated/flask.Request.html
@functions_framework.http
def podcast_search(request):
  """ """
  print(f"this is request.data - {request.data}")
  print(f"this is request.args - {request.args}")
  print(f"this is request.args.keys() - {request.args.keys()}")
  print(f"this is request.args.get('q') - {request.args.get('q')}")
  print(f"request.query_string {request.query_string}")
  if request.is_json:
    print(f"this is request.json - {request.json}")

  return 'OK'