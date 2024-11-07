from financialtrackerapp.app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False)

    # Financial record of the user
    balance = db.Column(db.Float, default=0.0)
    savings = db.Column(db.Float, default=0.0)
    budget = db.Column(db.Float, default=0.0)
    
    cart_items = db.relationship('CartItem', back_populates = 'user')
    
    
    def __repr__(self):
        return f" User {self.username} with the email {self.email}"
    
    def get_id(self):
        return self.uid
        