from sqlalchemy.ext.declarative import declared_attr
from flask.ext import restless
from flask import abort
from flangular import app, db
import core


manager = restless.APIManager(app, flask_sqlalchemy_db=db)

# Meta class to collect field information
class ModelMeta(type(db.Model)):
    def __new__(meta, name, bases, attrs):
        model = super(ModelMeta, meta).__new__(meta, name, bases, attrs)
        if not attrs.get('__abstract__', False):
            model.register()

        return model


class Model(db.Model):
    __metaclass__ = ModelMeta
    __abstract__ = True
    __url__ = False

    id = db.Column(db.Integer, primary_key=True)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @classmethod
    def register(cls):
        if cls.__url__:
            print 'Register Restless API for %s @ %s' % (cls, cls.__url__)
            blueprint = manager.create_api_blueprint(
                cls, methods=['GET', 'POST', 'PUT', 'DELETE'],
                collection_name=cls.__url__)

            blueprint.before_request(cls.before_request)
            app.register_blueprint(blueprint)

    @classmethod
    def before_request(cls):
        if not core.user_valid(cookie=False):
            abort(401)
