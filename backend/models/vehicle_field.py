from db import db

class VehicleField(db.Model):
    __tablename__ = "vehicle_field"

    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicles.id"))
    field_id = db.Column(db.Integer, db.ForeignKey("fields.id"))
    