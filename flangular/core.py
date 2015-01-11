from flask import request, render_template, flash, g, make_response, url_for, \
    redirect, send_from_directory, abort
from urlparse import urlparse, urljoin
from flangular import app
from user import User
import os

PRIVATE_FOLDER = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'private')


@app.errorhandler(404)
def error(err):
    return render_template('404.html'), 404


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


def get_redirect_target():
    return request.values.get('next', None)


def redirect_back(endpoint, **values):
    target = request.form['next']
    if not target or not is_safe_url(target):
        target = url_for(endpoint, **values)
    return redirect(target)


@app.route('/login', methods=('GET',))
def login_form():
    resp = make_response(render_template(
            'login.html', next=get_redirect_target()))

    # Reset session information to log user out, since the login page functions
    # also as logout page.
    g.user = None
    resp.set_cookie('XSRF-TOKEN', '', expires=0);
    return resp


@app.route('/login', methods=('POST',))
def login():
    user = User.login(request.form['email'], request.form['password'])
    if user is not None:
        g.user = user
        resp = make_response(redirect_back('index'))
        return resp

    flash('Could not log in.')
    return render_template('login.html')


@app.after_request
def after_request(resp):
    user = g.get('user', None)
    if user is not None:
        # refresh token
        token = user.generate_auth_token()
        resp.set_cookie('XSRF-TOKEN', token.decode('ascii'));

    return resp

def user_valid(cookie=False):
    if cookie:
        token = request.cookies.get('XSRF-TOKEN')
    else:
        token = request.headers.get('X-XSRF-TOKEN')

    if token is None:
        return None

    user = User.verify_auth_token(token)
    g.user = user
    return user

@app.route('/priv/<path:filename>')
def private_static(filename):
    if user_valid(cookie=True):
        return send_from_directory(PRIVATE_FOLDER, filename)
    else:
        abort(401)


@app.route('/')
def index():
    if user_valid(cookie=True):
        return private_static('flangular.html')
    else:
        return redirect('/login')

@app.after_request
def add_header(response):
    # prevent browser caching
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response
