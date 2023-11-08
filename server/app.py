from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['POST', 'GET'])
def messages():
    if request.method == "GET":
        return make_response(
            [message.to_dict() for message in Message.query.all()], 200
        )
    elif request.method == "POST":
        req = request.get_json()
        new_message = Message(body=req.get("body"), username=req.get("username"))

        db.session.add(new_message)
        db.session.commit()

        return make_response(
            new_message.to_dict(),201
        )

@app.route('/messages/<int:id>', methods=["PATCH", "DELETE"])
def messages_by_id(id):
    message = Message.query.filter(Message.id==id).first()
    if request.method == "PATCH":
        for attr in request.get_json():
            setattr(message, attr, request.get_json().get(attr))

        db.session.add(message)
        db.session.commit()

        return make_response(
            message.to_dict(), 200
        )
    
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.commit()
        return make_response(
            {"message": "succesfully deleted"}, 200
        )
    
    

if __name__ == '__main__':
    app.run(port=5555)
