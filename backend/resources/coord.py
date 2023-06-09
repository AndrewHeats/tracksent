import datetime
from flask import abort, render_template
from flask.views import MethodView
from flask_smorest import Blueprint
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import CoordModel
from schemas import CoordUpdateSchema, PlainCoordSchema, GetCoordSchema

blp = Blueprint("Coords", "coords", description="Operation on coords")

@blp.route("/coord/field=<int:field_id>&vehicle=<int:vehicle_id>")
class Coord(MethodView):
    def get(self, field_id, vehicle_id):
        coords = CoordModel.query.filter_by(vehicle_id=vehicle_id, field_id=field_id)
        points = [[coord.lat, coord.long] for coord in coords]
        print(points)
        # return render_template("index.html", points=points)
        return points

    @blp.response(
        202,
        description="Deletes a coord if no item is tagged with it.",
        example={"message": "Coord deleted."},
    )
    @blp.alt_response(404, description="Coord not found.")
    @blp.alt_response(
        400,
        description="Returned if the coord is assigned to one or more vehicles. In this case, the field is not deleted."
    )
    def delete(self, coord_id):
        coord = CoordModel.query.get_or_404(coord_id)
        if not coord.vehicles:
            db.session.delete(coord)
            db.session.commit()
            return {"message": "Coord deleted."}
        abort(400,
            message="Could not delete coord. Make sure coord is not associated with any items, then try again.",)

    @blp.arguments(CoordUpdateSchema)
    @blp.response(200, PlainCoordSchema)
    def put(self, coord_data, coord_id):
        coord = CoordModel.query.get(coord_id)

        if coord:
            coord.area = coord_data["area"]
        else:
            coord = CoordModel(id=coord_id, **coord_data)

        db.session.add(coord)
        db.session.commit()

        return coord

@blp.route("/coord")
class CoordList(MethodView):
    @blp.response(200, PlainCoordSchema(many=True))
    def get(self):
        coords = CoordModel.query.all()
        print(coords)
        return coords

    @blp.arguments(GetCoordSchema)
    @blp.response(200, PlainCoordSchema(many=True))
    def post(self, coord_data):
        coords = []
        for coord in CoordModel.query.filter_by(vehicle_id=coord_data["vehicle_id"],
                                            field_id=coord_data["field_id"]):
            if coord_data["datetime1"] < coord.datetime < coord_data["datetime2"]:
                coords.append(coords)

        print(coords)
        return coords

@blp.route("/coord/field_id=<int:field_id>&vehicle_id=<int:vehicle_id>&" + \
           "datetime=<string:datetime>&lat=<float:lat>&long=<float:long>&alt=<float:alt>")
def get_coord(**args):
    args["datetime"] = datetime.datetime.strptime(args["datetime"], '%m-%d-%y,%H:%M:%S')
    coord = CoordModel(**args)

    db.session.add(coord)
    db.session.commit()

    return "Coord has been sucessfuly writed"
