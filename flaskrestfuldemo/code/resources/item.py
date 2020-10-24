import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True,
                        help='This field cannot be left blank')

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': f'An item with name {name} already exists'}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'])
        try:
            item.save_to_db()
        except :
            return {'message':'An error occurred'},500
        return item.json(), 201

    # @jwt_required
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message':'Item deleted'}
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # query = "DELETE FROM items WHERE name = ?"
        # cursor.execute(query, (name,))
        # connection.commit()
        # connection.close()
        # return {'message': 'item deleted'}, 200


    # @jwt_required
    def put(self, name):
        # data = request.get_json()
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        # updated_item = ItemModel(name, data['price'])
        # {'name': name, 'price': data['price']}
        # item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = ItemModel(name, data['price'])
            # try:
                
                # updated_item.insert()
                # ItemModel.insert(updated_item)
            # except:
                # return {'message':"An error occurred while insertion"},500
            # item = {'name': name, 'price': data['price']}
            # items.append(item)
        else:
            item.price = data['price']
        item.save_to_db()
            # try:
                # updated_item.update()
                # ItemModel.update(updated_item)
            # except:
                # item.update(data)
                # return {'message': "An error occurred while updation"}, 500
        # return updated_item.json()
        return item.json()


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items =[]
        for row in result:
            items.append({'name':row[0],'price':row[1]})
        connection.commit()
        connection.close()
        return {'items': items}
