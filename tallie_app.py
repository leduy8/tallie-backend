from app import app, db
from app.models import User, Product, Payment, Wishlist, Seen, Picture, Category, Abuse, Helpful, Review

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db, 
        'User': User, 
        'Product': Product,
        'Payment': Payment,
        'Wishlist': Wishlist,
        'Seen': Seen,
        'Picture': Picture,
        'Category': Category,
        'Abuse': Abuse,
        'Helpful': Helpful,
        'Review': Review
    }

