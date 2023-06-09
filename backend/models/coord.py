from db import db

class CoordModel(db.Model):
    __tablename__ = "coords"

    id = db.Column(db.Integer, primary_key=True)
    field_id = db.Column(db.Integer)
    vehicle_id = db.Column(db.Integer)
    datetime = db.Column(db.DateTime(True))
    lat = db.Column(db.Float)
    long = db.Column(db.Float)
    alt = db.Column(db.Float)
