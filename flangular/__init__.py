import flask
import flask.ext.sqlalchemy
import config

app = flask.Flask(__name__)
app.config.from_object(config)
db = flask.ext.sqlalchemy.SQLAlchemy(app)

import core
import user
import computer

db.create_all()

# Create admim user if not exists
user.User.new_user(u'admin@flangular.js', u'admin')


