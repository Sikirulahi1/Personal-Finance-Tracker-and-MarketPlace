from financialtrackerapp.app import db

class Product(db.Model): 
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)  
    price = db.Column(db.Float, nullable=False)
    items_left = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(255)) 

    def __repr__(self):
        return f"<Product(id={self.id}, product_name='{self.product_name}', price=${self.price:.2f}, items_left={self.items_left})>"

    def get_id(self):  
        return self.id
    
    
class CartItem(db.Model):
    __tablename__ = 'cart_items'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable=False)
    product_id = db.Column(db.Integer, nullable= False)
    product_name = db.Column(db.String(100), nullable=False)  
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    
    user = db.relationship('User', back_populates='cart_items')

    def __repr__(self):
        return f"<Cart(id={self.id}, product_name='{self.product_name}', price=${self.price:.2f}, items_left={self.items_bought})>"
    
    def get_id(self):  
        return self.id
    

class TransactionItem(db.Model):
    __tablename__ = 'transaction_items'
    
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'), nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<TransactionItem(id={self.id}, product_name='{self.product_name}', price=${self.price:.2f}>"
    
    def get_id(self):  
        return self.id