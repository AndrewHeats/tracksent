from flask import abort
from flask.views import MethodView
from flask_smorest import Blueprint
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import VehicleModel
from schemas import VehicleSchema, VehicleUpdateSchema, PlainVehicleSchema

blp = Blueprint("Vehicles", "vehicles", description="Operation on vehicles")


@blp.route("/vehicle/<string:vehicle_id>")
class Vehicle(MethodView):
    @blp.response(200, PlainVehicleSchema)
    def get(self, vehicle_id):
        vehicle = VehicleModel.query.get_or_404(vehicle_id)
        return vehicle

    def get_coordinates(self, vehicle_id):
        vehicle = VehicleModel.query.get_or_404(vehicle_id)
        coordinates = vehicle["coordinates"]
        result = coordinates["height"] + " " + coordinates["width"] + " " + coordinates["long"]
        return result

    def delete(self, vehicle_id):
        vehicle = VehicleModel.query.get_or_404(vehicle_id)
        db.session.delete(vehicle)
        db.session.close()
        return {"message": "Vehicle deleted succesfully"}

    @blp.arguments(VehicleUpdateSchema)
    @blp.response(200, PlainVehicleSchema)
    def put(self, vehicle_data, vehicle_id):
        vehicle = VehicleModel.query.get(vehicle_id)

        if vehicle:
            vehicle.name_of_owner = vehicle_data["name_of_owner"]
            vehicle.type = vehicle_data["type"]
        else:
            vehicle = VehicleModel(id=vehicle_id, **vehicle_data)

        db.session.add(vehicle)
        db.session.commit()

        return vehicle

@blp.route("/vehicle")
class VehicleList(MethodView):
    @blp.response(200, PlainVehicleSchema(many=True))
    def get(self):
        return VehicleModel.query.all()

    @blp.arguments(PlainVehicleSchema)
    @blp.response(201, PlainVehicleSchema)
    def post(self, vehicle_data):
        vehicle = VehicleModel(**vehicle_data)

        try:
            db.session.add(vehicle)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")

        return vehicle


'''@blp.route("/vehicle/<string:vehicle_id>/<int:time>")
class VehicleCoordinates(MethodView):
    def get(self, vehicle_id, time):
        vehicle = VehicleModel.query.get_or_404(vehicle_id)
        coordinates = vehicle["coordinates"]["time"]
        result = coordinates["height"] + " " + coordinates["width"] + " " + coordinates["long"]
        return result
'''
