from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from pymongo import MongoClient
import base64
import os


carousel_routes = Blueprint('carousel_routes', __name__)


client = MongoClient(os.getenv('MONGODB_URI'))
db = client.get_database()
carousel_collection = db['carruselimages']


@carousel_routes.route('/', methods=['POST'])
def upload_image():
    try:
        
        image = ''
        if 'image' in request.files:
            image_file = request.files['image']
            image = f"data:{image_file.mimetype};base64,{base64.b64encode(image_file.read()).decode()}"

        
        new_image = {
            'image': image
        }
        carousel_collection.insert_one(new_image)

        return jsonify(new_image), 201

    except Exception as e:
        return jsonify({'message': str(e)}), 500


@carousel_routes.route('/', methods=['GET'])
def get_images():
    try:
        images = list(carousel_collection.find())
        for image in images:
            image['_id'] = str(image['_id'])  
        return jsonify(images)

    except Exception as e:
        return jsonify({'message': str(e)}), 500
