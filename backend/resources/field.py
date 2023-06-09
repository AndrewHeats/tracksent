from flask import abort
from flask.views import MethodView
from flask_smorest import Blueprint
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import FieldModel, VehicleModel
from schemas import FieldSchema, FieldUpdateSchema, VehicleAndFieldSchema, PlainFieldSchema

blp = Blueprint("Fields", "fields", description="Operation on fields")


@blp.route("/field/<string:field_id>")
class Field(MethodView):
    @blp.response(200, PlainFieldSchema)
    def get(self, field_id):
        field = FieldModel.query.get_or_404(field_id)
        return field

    @blp.response(
        202,
        description="Deletes a field if no item is tagged with it.",
        example={"message": "Field deleted."},
    )
    @blp.alt_response(404, description="Field not found.")
    @blp.alt_response(
        400,
        description="Returned if the field is assigned to one or more vehicles. In this case, the field is not deleted."
        ,
    )
    def delete(self, field_id):
        field = FieldModel.query.get_or_404(field_id)
        if not field.vehicles:
            db.session.delete(field)
            db.session.commit()
            return {"message": "Field deleted."}
        abort(400,
            message="Could not delete field. Make sure field is not associated with any items, then try again.",)

    @blp.arguments(FieldUpdateSchema)
    @blp.response(200, PlainFieldSchema)
    def put(self, field_data, field_id):
        print("PUT requet")
        print(field_id)
        field = FieldModel.query.get(field_id)

        if field:
            field.area = field_data["area"]
        else:
            field = FieldModel(id=field_id, **field_data)

        db.session.add(field)
        db.session.commit()

        return field


@blp.route("/field")
class FieldList(MethodView):
    @blp.response(200, PlainFieldSchema)
    def get(self):
        return FieldModel.query.all()

    @blp.arguments(PlainFieldSchema)
    @blp.response(201, PlainFieldSchema)
    def post(self, field_data):
        field = FieldModel(**field_data)

        try:
            db.session.add(field)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")

        return field


# @blp.route("/vehicle/<string:vehicle_id>/field/<string:field_id>")
# class LinkTagsToItem(MethodView):
#     @blp.response(201, FieldSchema)
#     def post(self, vehicle_id, field_id):
#         vehicle = VehicleModel.query.get_or_404(vehicle_id)
#         field = FieldModel.query.get_or_404(field_id)

#         vehicle.fields.append(field)

#         try:
#             db.session.add(vehicle)
#             db.session.commit()
#         except SQLAlchemyError:
#             abort(500, message="An error occurred while inserting the field.")

#         return field

#     @blp.response(200, VehicleAndFieldSchema)
#     def delete(self, vehicle_id, field_id):
#         vehicle = VehicleModel.query.get_or_404(vehicle_id)
#         field = FieldModel.query.get_or_404(field_id)

#         vehicle.fields.remove(field)

#         try:
#             db.session.add(vehicle)
#             db.session.commit()
#         except SQLAlchemyError:
#             abort(500, message="An error occurred while inserting the field.")

#         return {"message": "vehicle removed from field", "vehicle": vehicle, "field": field}
