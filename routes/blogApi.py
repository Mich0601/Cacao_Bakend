import base64
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
import os


load_dotenv()


articulo_routes = Blueprint('articulo_routes', __name__)


client = MongoClient(os.getenv('MONGODB_URI'))
db = client.get_database()
articulos_collection = db['articulos']  

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

def convert_to_base64(file):
    
    return f"data:{file.mimetype};base64,{base64.b64encode(file.read()).decode()}"


@articulo_routes.route('/', methods=['POST'])
def crear_articulo():
    try:
        title = request.form.get('title')
        category = request.form.get('category')
        short_description = request.form.get('short_description')
        long_description = request.form.get('long_description')

       
        small_image = ''
        large_image = ''
        if 'small_image' in request.files:
            small_image_file = request.files['small_image']
            if allowed_file(small_image_file.filename):
                small_image = convert_to_base64(small_image_file)
            else:
                return jsonify({'error': 'Archivo de imagen pequeña no permitido'}), 400

        if 'large_image' in request.files:
            large_image_file = request.files['large_image']
            if allowed_file(large_image_file.filename):
                large_image = convert_to_base64(large_image_file)
            else:
                return jsonify({'error': 'Archivo de imagen grande no permitido'}), 400

        
        new_articulo = {
            'title': title,
            'category': category,
            'ShortD': short_description,
            'LongD': long_description,
            'ShortImg': small_image,
            'LongImg': large_image
        }
        result = articulos_collection.insert_one(new_articulo)
        new_articulo['_id'] = str(result.inserted_id)

        return jsonify(new_articulo), 201

    except Exception as e:
        return jsonify({'message': str(e)}), 500


@articulo_routes.route('/', methods=['GET'])
def listar_articulos():
    try:
        articulos = list(articulos_collection.find())
        for articulo in articulos:
            articulo['_id'] = str(articulo['_id'])  
        return jsonify(articulos)

    except Exception as e:
        return jsonify({'message': str(e)}), 500


@articulo_routes.route('/<id>', methods=['PUT'])
def actualizar_articulo(id):
    try:
        title = request.form.get('title')
        category = request.form.get('category')
        short_description = request.form.get('short_description')
        long_description = request.form.get('long_description')

        
        small_image = None
        large_image = None
        if 'small_image' in request.files:
            small_image_file = request.files['small_image']
            if allowed_file(small_image_file.filename):
                small_image = convert_to_base64(small_image_file)
            else:
                return jsonify({'error': 'Archivo de imagen pequeña no permitido'}), 400

        if 'large_image' in request.files:
            large_image_file = request.files['large_image']
            if allowed_file(large_image_file.filename):
                large_image = convert_to_base64(large_image_file)
            else:
                return jsonify({'error': 'Archivo de imagen grande no permitido'}), 400

       
        update_fields = {
            'title': title,
            'category': category,
            'ShortD': short_description,
            'LongD': long_description
        }
        if small_image is not None:
            update_fields['ShortImg'] = small_image
        if large_image is not None:
            update_fields['LongImg'] = large_image

        result = articulos_collection.update_one({'_id': ObjectId(id)}, {'$set': update_fields})

        if result.matched_count == 0:
            return jsonify({'error': 'Artículo no encontrado'}), 404

        
        updated_articulo = articulos_collection.find_one({'_id': ObjectId(id)})
        updated_articulo['_id'] = str(updated_articulo['_id'])

        return jsonify(updated_articulo), 200

    except Exception as e:
        return jsonify({'message': str(e)}), 500


@articulo_routes.route('/<id>', methods=['DELETE'])
def eliminar_articulo(id):
    try:
        result = articulos_collection.delete_one({'_id': ObjectId(id)})
        
        if result.deleted_count == 0:
            return jsonify({'error': 'Artículo no encontrado'}), 404

        return jsonify({'mensaje': 'Artículo eliminado'}), 200

    except Exception as e:
        return jsonify({'message': str(e)}), 500