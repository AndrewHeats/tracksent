from db import db

class FieldModel(db.Model):
    __tablename__ = "fields"

    id = db.Column(db.Integer, primary_key=True)
    area = db.Column(db.Float(precision=2), nullable=False)
    process = db.Column(db.String, nullable=False)
    plant = db.Column(db.String, nullable=False)
