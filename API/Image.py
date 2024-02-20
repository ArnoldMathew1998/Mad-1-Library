from flask_restful import Resource, reqparse, marshal_with, fields
from Database.models import db, Image


image_fields = {
    'image_id': fields.Integer,
    'image_data': fields.String,
    'pdf_data': fields.String,
    'book_id': fields.Integer
}

Image_api_parser = reqparse.RequestParser()
Image_api_parser.add_argument('image_data', type=str, help='Image data (in base64 format)')
Image_api_parser.add_argument('pdf_data', type=str, help='PDF data (in base64 format)')
Image_api_parser.add_argument('book_id', type=int, help='ID of the associated book')


class Image_api(Resource):
    @marshal_with(image_fields)
    def get(self, image_id):
        image = Image.query.get(image_id)
        if image:
            return image
        else:
            return {'message': 'Image not found'}, 404

    def post(self):
        Image_api_args = Image_api_parser.parse_args()
        new_image = Image(
            image_data=Image_api_args['image_data'].encode('utf-8') if Image_api_args['image_data'] else None,
            pdf_data=Image_api_args['pdf_data'].encode('utf-8') if Image_api_args['pdf_data'] else None,
            book_id=Image_api_args['book_id']
        )
        db.session.add(new_image)
        db.session.commit()
        return {'message': 'Image Added successfully'}, 201

    def put(self, image_id):
        Image_api_args = Image_api_parser.parse_args()
        image = Image.query.get(image_id)
        if image:
            image.image_data = Image_api_args['image_data'].encode('utf-8') if Image_api_args['image_data'] else None
            image.pdf_data = Image_api_args['pdf_data'].encode('utf-8') if Image_api_args['pdf_data'] else None
            image.book_id = Image_api_args['book_id']
            db.session.commit()
            return {'message': 'Image updated successfully'}, 201
        else:
            return {'message': 'Image not found'}, 404

    def delete(self, image_id):
        image = Image.query.get(image_id)
        if image:
            db.session.delete(image)
            db.session.commit()
            return {'message': 'Image deleted successfully'}, 201
        else:
            return {'message': 'Image not found'}, 404
