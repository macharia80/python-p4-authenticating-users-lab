# seed.py
from app import app
from models import db, User

with app.app_context():
    # Clear existing data
    User.query.delete()
    
    # Create test users
    users = [
        User(username="alice"),
        User(username="bob"),
        User(username="charlie")
    ]
    
    # Add to database
    db.session.add_all(users)
    db.session.commit()