import os

from flask import Flask,redirect
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    auth = HTTPBasicAuth()

    users = {
        "admin": generate_password_hash("2222"),
    }

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @auth.verify_password
    def verify_password(username, password):
        if username in users and \
                check_password_hash(users.get(username), password):
            return username

    # a simple page that says hello
    @app.route('/')
    @auth.login_required
    def hello():
        return redirect('index')

    if __name__ == '__main__':
        app.run()

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/index', endpoint='index')

    return app