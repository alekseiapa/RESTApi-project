from flask_restful import Resource
from models.store import StoreModel


class Store(Resource):

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {"message": f"Store {name} not found!"}


    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"message": f"Store {name} already exists!"}
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred to create the store!"}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {"message": f"Store {name} deleted from the database"}

        return {"message": f"Store {name} doesn't exist!"}


class StoreList(Resource):
    def get(self):
        return {"stores": [store.json() for store in StoreModel.query.all()]}