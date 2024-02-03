from flask_restful import Resource, fields, marshal_with, reqparse
from Database.models import db,Image



Image_api_parser = reqparse.RequestParser()
Image_api_parser.add_argument('data', type=str, help='Image data (in base64 format)')
Image_api_parser.add_argument('book_id', type=int, help='ID of the associated book')



class Image_api(Resource):
    def get(self, image_id):
        image = Image.query.get(image_id)
        if image:
            return image
        else:
            return {'message': 'Image not found'}, 404
    def post(self):
        Image_api_args = Image_api_parser.parse_args()
        new_image = Image(
            data=Image_api_args['data'].encode('utf-8'),  # Convert base64 string to bytes
            book_id=Image_api_args['book_id']
        )
        db.session.add(new_image)
        db.session.commit()
        return new_image, 201
    def put(self, image_id):
        Image_api_args = Image_api_parser.parse_args()
        image = Image.query.get(image_id)
        if image:
            image.data = Image_api_args['data'].encode('utf-8')  # Convert base64 string to bytes
            image.book_id = Image_api_args['book_id']
            db.session.commit()
            return image
        else:
            return {'message': 'Image not found'}, 404
    def delete(self, image_id):
        image = Image.query.get(image_id)
        if image:
            db.session.delete(image)
            db.session.commit()
            return {'message': 'Image deleted successfully'}
        else:
            return {'message': 'Image not found'}, 404

