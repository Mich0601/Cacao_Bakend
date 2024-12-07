import base64
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from pymongo import MongoClient
import json
import os

product_routes = Blueprint('product_routes', __name__)
client = MongoClient(os.getenv('MONGODB_URI'))
db = client.get_database()
products_collection = db['products']

def archivo_permitido(filename):
    return
@product_routes.route('/', methods=['POST'])
def create_product():
    try:
        title = request.form.get('title')
        description = request.form.get('description')
        precio = request.form.get('precio')

       
        try:
            parsed_precio = json.loads(precio)
        except json.JSONDecodeError:
            parsed_precio = float(precio) if precio.replace('.', '', 1).isdigit() else precio

        image = ''
        if 'image' in request.files:
            image_file = request.files['image']
            image = f"data:{image_file.mimetype};base64,{base64.b64encode(image_file.read()).decode()}"

        
        new_product = {
            'title': title,
            'description': description,
            'precio': parsed_precio,
            'image': image
        }
        products_collection.insert_one(new_product)

        return jsonify(new_product), 201

    except Exception as e:
        return jsonify({'message': str(e)}), 500


@product_routes.route('/', methods=['GET'])
def get_products():
    try:
        products = list(products_collection.find())
        for product in products:
            product['_id'] = str(product['_id'])  
        return jsonify(products)

    except Exception as e:
        return jsonify({'message': str(e)}), 500