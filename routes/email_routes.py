from flask import Blueprint, render_template, request, jsonify, current_app
from flask_mail import Message


email_bp = Blueprint('email_bp', __name__, template_folder='templates')


@email_bp.route('/send', methods=['POST'])
def send_email():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    message_content = data.get('message')

    print(f"Enviando correo a: {email}")
    print(f"Contenido del mensaje: {message_content}")

  
    msg = Message(subject=f"Mensaje de {name}",
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[email])

    
    msg.html = render_template('templatecontact.html', name=name, email=email, message=message_content)

    try:
        
        current_app.extensions['mail'].send(msg)
        print("Correo enviado con éxito")
        return jsonify({"message": "Correo enviado con éxito"}), 200
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
        return jsonify({
            "message": "Lo sentimos. No se ha logrado enviar correctamente su contacto, por favor intente nuevamente.",
            "retry": True
        }), 500
