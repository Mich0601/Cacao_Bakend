from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)  
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')  
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)  

client = MongoClient(os.getenv('MONGODB_URI'))
db = client.get_database()

UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from routes.product_routes import product_routes
from routes.carousel_routes import carousel_routes
from routes.coments import commentscarrusel_routes
from routes.event_routes import event_routes  
from routes.blogApi import articulo_routes
from routes.email_routes import email_bp

app.register_blueprint(product_routes, url_prefix='/api/products')
app.register_blueprint(carousel_routes, url_prefix='/api/carrusel')
app.register_blueprint(commentscarrusel_routes, url_prefix='/api/commentscarrusel')
app.register_blueprint(event_routes, url_prefix='/api/events')  
app.register_blueprint(articulo_routes, url_prefix='/api/articulo')
app.register_blueprint(email_bp, url_prefix='/api/email')


@app.route('/')
def index():
    return 'Servidor en funcionamiento'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if __name__ == '__main__':
    app.run(port=3000, debug=True)
