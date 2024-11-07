# from financialtrackerapp.app import db
# from datetime import datetime

# class Transaction(db.Model):
#     __tablename__ = 'transactions'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     total_amount = db.Column(db.Float, nullable=False)
#     date = db.Column(db.DateTime, default=datetime.utcnow)
#     status = db.Column(db.String(20), nullable=False, default='Completed')
#     transaction_type = db.Column(db.String(20), nullable=False)
#     items = db.relationship('TransactionItem', backref='transaction', lazy=True)
    