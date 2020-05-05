from flask import render_template
from flask import request
from variables import cookies

import time
import flask
from flask import Flask
app = Flask(__name__)

import requests
MEMRISE_ENDPOINT = "https://www.memrise.com"

@app.route('/', methods=("GET", "POST", "OPTIONS"))
def index():
  qs=request.query_string

  if qs:
    try:
      qs = qs.decode('utf8')

      agent = request.headers.get('User-Agent')
      oauth = request.headers.get('Authorization')
      ctype = request.headers.get('Content-Type')
      csrftoken = request.headers.get('X-CSRFToken')
      
      headers = {}
      headers['Referer'] = MEMRISE_ENDPOINT
      if agent is not None:
        headers['User-Agent'] = agent
      if oauth is not None:
        headers['Authorization'] = oauth
      if csrftoken is not None:
        headers['X-CSRFToken'] = csrftoken
      headers['X-CSRFToken'] = cookies['csrftoken']
      print(headers)


      if request.method == "POST":
        user_data = {}
          
        if 'application/json' in ctype:
          user_data = request.data
        else:
          user_data = request.form.to_dict()

        if 'multipart/form-data' in ctype:
          user_files = request.files.to_dict()

          r = requests.post(qs, headers = headers, cookies=cookies, data = user_data, files = user_files)
        else:
          r = requests.post(qs, headers = headers, cookies=cookies, data = user_data)
      elif request.method == "GET":
        r = requests.get(qs, headers = headers)
      elif request.method == "OPTIONS":
        '''
        OPTIONS has recently been used before POST in some libraries
        but not all websites have an OPTIONS http method; therefore,
        we provide a request to ourself in order to return
        the correct headers with correct response code and data
        '''
        r = requests.options(request.base_url, cookies=cookies, headers = headers)

      rt = r.text
    except:
      return "nope"

    response = flask.Response(rt)
    status_code = r.status_code

    '''
    we don't really care if the requests.options above 
    returns an OK request or not, we just care about
    passing a new response with new headers, and a valid status code
    '''
    if request.method == "OPTIONS":
      status_code = 200

    response.headers['Access-Control-Allow-Origin'] = '*'
    
    # ensure that data getting passed back is plain text
    response.headers['Content-Type'] = "text/plain"
    
    '''
    preflight CORS policy response headers
      - Returns Allowed Methods:
          In our case, GET and POST are the only ones allowed
      - Returns Allowed Headers:
          In our case, it is the headers that the user requested to use
          so, the ones in Access-Control-Request-Headers
    '''
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = request.headers.get('Access-Control-Request-Headers')
    
    return response, status_code
  else:
    print("nope")

  return render_template('index.html')

