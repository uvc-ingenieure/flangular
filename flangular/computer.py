from flangular import db
from .model import Model

class Computer(Model):
    __url__ = 'computer'

    processor = db.Column(db.Unicode)
    ram = db.Column(db.Unicode)
    power = db.Column(db.Unicode)
