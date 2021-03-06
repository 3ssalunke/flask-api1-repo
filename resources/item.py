from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field cannot be left blank'
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help='This field cannot be left blank'
                        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'item not found'}, 404

    @jwt_required()
    def post(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return {'message': 'Item already exists.'}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
            return {'message': f'item {name} inserted succesfully'}
        except:
            return {'message': 'An Error Occurred'}, 500

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': f'item {name} deleted succesfully'}
        return {'message': 'An Error Occured'}, 500

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
        item.save_to_db()
        return {'message': f'item {name} upserted succesfully'}


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
