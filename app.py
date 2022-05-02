'''This is a flask app micro service for the dev ops culture and practice course'''
from flask import Flask, render_template, jsonify
from flask_bootstrap import Bootstrap
from werkzeug.middleware.dispatcher import DispatcherMiddleware # pylint: disable=no-name-in-module
from prometheus_client import make_wsgi_app, Counter

app = Flask(__name__)

# Add prometheus wsgi middleware to route /metrics requests
APP_DISPATCH = DispatcherMiddleware(app, {
    '/metrics/': make_wsgi_app()
})

COUNTER_API_HELLO = Counter('api_gets', 'How many times someone visits /api/hello/')

Bootstrap(app)

# The website version
@app.route('/')
@app.route('/<username>')
def home_page(username='World!'):
    '''A function that renders a web page.  If you user the /<username>
       endpoint the web page will include that word
        :param username: The username of the user.  Defaults to
                         World! if no username is supplied.
        :type username:  String.

        :rtype: An HTML page loaded from templates/home.html
    '''
    COUNTER_API_HELLO.inc()
    return render_template('home.html', username=username)

# The json microservice version
@app.route('/api/hello/')
@app.route('/api/hello/<username>')
def api(username='World!'):
    '''A function that returns some json.  The default is a
       dictionary containing Hello: World!  If the
       /api/<user> endpoint is hit then you get a more
       interesting response.

        :param username: The username of the user.  Defaults to
                         World! if no username is supplied.
        :type username:  String.

        :rtype: A dictionary object containing Hello: <username>.
    '''
    return jsonify({'Hello': username})

@app.route('/api/version/')
def version():
    '''This function returns a dictionary containing only
       the key version with a value set to the application
       version number which is read from a file called VERSION.txt

       The VERSION.txt file is read and the variable version is
       extracted by taking the first line ([0]) and then removing
       any whitespace (like \n from it) with strip().  It's not
       converted to an integer because sometimes versions have letters,
       or dots in them.

       :rtype: A Json object containing version: number
    '''
    with open("VERSION.txt", "r", encoding="utf-8") as myfile:
        version_number = myfile.readlines()[0].strip()

    return jsonify({'version': version_number})
