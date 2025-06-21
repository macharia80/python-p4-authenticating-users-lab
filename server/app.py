# app.py
from flask import Flask, request, session
from flask_restful import Api, Resource
from models import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# Setup session secret key
app.secret_key = 'your_secret_key_here'

api = Api(app)

db.init_app(app)

with app.app_context():
    db.create_all()

class Login(Resource):
    def post(self):
        username = request.get_json().get('username')
        user = User.query.filter_by(username=username).first()
        
        if user:
            session['user_id'] = user.id
            return user.to_dict(), 200
        else:
            return {"error": "User not found"}, 401

class Logout(Resource):
    def delete(self):
        session.pop('user_id', None)
        return '', 204

class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
        if user_id:
            user = User.query.get(user_id)
            return user.to_dict(), 200
        else:
            return '', 401

class Posts(Resource):
    def get(self):
        return [
            {"id": 1, "title": "My First Post", "content": "This is my first post!"},
            {"id": 2, "title": "My Second Post", "content": "This is my second post!"}
        ], 200

# Add resources
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(CheckSession, '/check_session')
api.add_resource(Posts, '/posts')

if __name__ == '__main__':
    app.run(port=5555, debug=True)