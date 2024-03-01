from flask_restful import Resource, reqparse,request
from Database.models import db,Image


image_parser = reqparse.RequestParser()
image_parser.add_argument('image_data', type=str, required=True, help='Base64-encoded image data')
image_parser.add_argument('book_id', type=int, help='ID of the associated book')
image_parser.add_argument('sec_id', type=int, help='ID of the associated Section')

class Image_api(Resource):
    def get(self, book_id):
        image = Image.query.get(book_id)
        if image:
            return {'image_data': image.image_data}
        else:
            return {'message': 'Image not found'}, 404

    def post(self, book_id, sec_id):
        args = image_parser.parse_args()
        image_data = args['image_data']
        new_image = Image(image_data=image_data, book_id=book_id , sec_id=sec_id)
        db.session.add(new_image)
        db.session.commit()

        return {'message': 'Image uploaded successfully'}, 201
    
    def put(self, book_id):
        args = image_parser.parse_args()
        image = Image.query.get(book_id)
        image_data = args['image_data']

        if image:
            image.image_data = image_data
        db.session.commit()
        return {'message': 'Image uploaded successfully'}, 201
    
    def delete(self, book_id=None, sec_id=None):
        if sec_id:
            Image.query.filter_by(sec_id=sec_id).delete()
            db.session.commit()
            return {'message': 'Image deleted successfully'}, 201
        if book_id:
            Image.query.filter_by(book_id=book_id).delete()
            db.session.commit()
            return {'message': 'Image deleted successfully'}, 201
        return {'message': ' not found'}, 404
