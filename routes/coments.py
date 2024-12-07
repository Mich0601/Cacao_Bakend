from datetime import datetime
from bson import ObjectId
from flask import Flask, Blueprint, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS
import os


commentscarrusel_routes = Blueprint('commentscarrusel', __name__)

MONGO_URI = os.getenv('MONGODB_URI') or "mongodb+srv://Michelle:Mich0601@cluster0.iq4zu.mongodb.net/commentsDB?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client['commentsDB']
temporary_comments_collection = db['comments_Temporary']
approved_comments_collection = db['comments']
rejected_comments_collection = db['rejectedcoment']

@commentscarrusel_routes.route('/', methods=['GET'])
def get_approved_comments():
    try:
        
        comments = list(approved_comments_collection.find({'status': 'approved'}))
        
        for comment in comments:
            comment['_id'] = str(comment['_id'])
        
        return jsonify(comments)
    except Exception as e:
        
        print(f'Error al obtener comentarios: {str(e)}')
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500




@commentscarrusel_routes.route('/add_commentU', methods=['POST'])
def add_comment():
    try:
        username = request.form['username']
        comment = request.form['comment']
        source = request.form.get('source', 'Comentarios Clientes') 

        if not username or not comment:
            return jsonify({'error': 'Username and comment are required'}), 400

        new_comment = {
            'username': username,
            'comment': comment,
            'source': source,  
            'status': 'pending',
            'created_at': datetime.utcnow()
        }
        temporary_comments_collection.insert_one(new_comment)
        return jsonify({'message': 'Comment submitted successfully'}), 201
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

    

@commentscarrusel_routes.route('/temporary-commentsU', methods=['GET'])
def get_temporary_commentsU():
    try:
        temporary_commentsU = list(temporary_comments_collection.find({'status': 'pending'}))
        for comment in temporary_commentsU:
            comment['_id'] = str(comment['_id'])
            comment['created_at'] = comment['created_at'].strftime('%Y-%m-%d %H:%M:%S')
        return jsonify(temporary_commentsU)
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500



@commentscarrusel_routes.route('/approve/<id>', methods=['POST'])
def approve_comment(id):
    try:
        comment = temporary_comments_collection.find_one_and_delete({'_id': ObjectId(id)})
        if comment:
            comment['status'] = 'approved'
            comment['approved_at'] = datetime.utcnow()
            approved_comments_collection.insert_one(comment)
            return jsonify({'message': 'Comment approved'}), 200
        else:
            return jsonify({'error': 'Comment not found'}), 404
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


@commentscarrusel_routes.route('/reject/<id>', methods=['POST'])
def reject_comment(id):
    try:
        comment = temporary_comments_collection.find_one_and_delete({'_id': ObjectId(id)})
        if comment:
            comment['status'] = 'rejected'
            rejected_comments_collection.insert_one(comment)
            return jsonify({'message': 'Comment rejected'}), 200
        else:
            return jsonify({'error': 'Comment not found'}), 404
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500
    
    

@commentscarrusel_routes.route('/add_product/<product_id>', methods=['POST'])
def add_product_comment(product_id):
    try:
        
        print(request.json)  
        username = request.json['username']
        comment = request.json['comment']
        source = request.json.get('source', 'Comentarios Productos')  

        if not username or not comment:
            return jsonify({'error': 'Username and comment are required'}), 400

        new_comment = {
            'username': username,
            'comment': comment,
            'product_id': product_id,  
            'source': source,
            'status': 'pending',
            'created_at': datetime.utcnow()
        }
        temporary_comments_collection.insert_one(new_comment)
        return jsonify({'message': 'Comment for product submitted successfully'}), 201
    except Exception as e:
        print(f'Error: {str(e)}')  
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500




@commentscarrusel_routes.route('/product_comments/<product_id>', methods=['GET'])
def get_product_comments(product_id):
    try:
        
        comments = list(approved_comments_collection.find({
            'product_id': product_id,
            'status': 'approved'
        }))
        
        
        for comment in comments:
            comment['_id'] = str(comment['_id'])
            comment['created_at'] = comment['created_at'].strftime('%Y-%m-%d %H:%M:%S')
        return jsonify(comments)
    except Exception as e:
        print(f'Error al obtener comentarios del producto: {str(e)}')
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500



app = Flask(__name__)
app.register_blueprint(commentscarrusel_routes)


CORS(app)


if __name__ == '_main_':
    app.run(debug=True)