
from flask import Blueprint, request, jsonify, render_template
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime


event_routes = Blueprint('event_routes', __name__)


client = MongoClient("mongodb+srv://Michelle:Mich0601@cluster0.iq4zu.mongodb.net/commentsDB?retryWrites=true&w=majority")
db = client['commentsDB']
events_collection = db['Eventos']


@event_routes.route('/add_event', methods=['POST'])
def add_event():
    try:
        data = request.json
        title = data.get('title')
        date = data.get('date')
        time = data.get('time')
        direccion = data.get('direccion')
        ubicacion = data.get('ubicacion')
        status = data.get('status')
        shortDescription = data.get('shortDescription')
        longDescription = data.get('longDescription')
        image = data.get('image')

        if title and date and time and image:
            event = {
                'title': title,
                'date': date,
                'time': time,
                'direccion': direccion,
                'ubicacion': ubicacion,
                'status': status,
                'shortDescription': shortDescription,
                'longDescription': longDescription,
                'image': image,
                'created_at': datetime.datetime.now()
            }
            result = events_collection.insert_one(event)
            return jsonify({'message': 'Evento agregado', 'id': str(result.inserted_id)}), 201
        return jsonify({'error': 'Datos incompletos'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@event_routes.route('/events', methods=['GET'])
def get_events():
    try:
        events = list(events_collection.find())
        for event in events:
            event['_id'] = str(event['_id'])
        return jsonify(events)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@event_routes.route('/events/<id>', methods=['GET'])
def get_event(id):
    try:
        event = events_collection.find_one({'_id': ObjectId(id)})
        if event:
            event['_id'] = str(event['_id'])
            return jsonify(event)
        return jsonify({'error': 'Evento no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@event_routes.route('/edit_event/<id>', methods=['PUT'])
def edit_event(id):
    try:
        data = request.json
        title = data.get('title')
        date = data.get('date')
        time = data.get('time')
        direccion = data.get('direccion')
        ubicacion = data.get('ubicacion')
        status = data.get('status')
        shortDescription = data.get('shortDescription')
        longDescription = data.get('longDescription')
        image = data.get('image')

        update_data = {
            'title': title,
            'date': date,
            'time': time,
            'direccion': direccion,
            'ubicacion': ubicacion,
            'status': status,
            'shortDescription': shortDescription,
            'longDescription': longDescription,
            'image': image,
        }

        result = events_collection.update_one({'_id': ObjectId(id)}, {'$set': update_data})
        if result.modified_count > 0:
            return jsonify({'message': 'Evento actualizado'}), 200
        return jsonify({'error': 'No se encontraron cambios'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@event_routes.route('/delete_event/<id>', methods=['DELETE'])
def delete_event(id):
    try:
        result = events_collection.delete_one({'_id': ObjectId(id)})
        if result.deleted_count == 1:
            return jsonify({'message': 'Evento eliminado'}), 200
        return jsonify({'error': 'Evento no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
