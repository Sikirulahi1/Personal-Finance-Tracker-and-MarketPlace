import pandas as pd
from financialtrackerapp.app import create_app, db
from financialtrackerapp.blueprints.marketplace.models import Product

# Load CSV data
data = pd.read_csv('jumia_product_processed.csv')

# Data cleaning
data['Product'] = data['Product'].str.strip()  # Strip extra whitespace
# data['Price'] = data['Price'].replace('[\$,]', '', regex=True).astype(float)
data['Items_left'] = data['Items_left'].astype(int)  # Ensure integer type for items left

# Initialize Flask app and use the app context
app = create_app()

with app.app_context():
    try:
        # Insert cleaned data into the database
        for _, row in data.iterrows():
            product = Product(
                id=row['id'],
                product_name=row['Product'],
                price=row['Price'],
                items_left=row['Items_left'],
                image_url=row['Image_url']
            )
            db.session.add(product)

        # Commit the session to save changes
        db.session.commit()
        print("Data successfully added to the database.")
    
    except Exception as e:
        # Roll back in case of error
        db.session.rollback()
        print(f"An error occurred: {e}")
