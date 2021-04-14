from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
                        type=float,
                        required=True,
                        help="This field can not be empty"

                        )
    parser.add_argument("store_id",
                        type=int,
                        required=True,
                        help="Each item needs a store_id"

                        )
    @jwt_required()
    def get(self, name):
        try:
            item = ItemModel.find_item_by_name(name)
            if item:
                return item.json()
            else:
                return {"message": f"item {name} not found"}, 404
        except:
            return {"message": "Authentication required"}, 401
    def post(self, name):
        if ItemModel.find_item_by_name(name):
            return {"message": f"This item {name} already exists"}, 400
        data = Item.parser.parse_args()
        new_item = ItemModel(name, data["price"], data["store_id"])
        try:
            new_item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item"}, 500
        return new_item.json(), 201



    def delete(self, name):
        item = ItemModel.find_item_by_name(name)
        if not item:
            return {"message": "This item not found"}
        item.delete_from_db()
        return {"message": f"Item {name} successfully deleted"}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_item_by_name(name)

        if item is None:
            try:
                item = ItemModel(name, data["price"], data["store_id"])
            except:
                return {"message": "An error occurred inserting the item"}, 500
        else:
            try:
                item.price = data["price"]
            except:
                return {"message": "An error occurred inserting the item"}, 500

        item.save_to_db()
        return item.json()




class ItemsList(Resource):
    @jwt_required()
    def get(self):
        try:
            return {"items": [item.json() for item in ItemModel.query.all()]}
        except:
            return {"message": "Authentication required"}, 401