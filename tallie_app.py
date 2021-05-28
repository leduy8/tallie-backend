from app import app, db
from app.models import User, Product, Payment, Wishlist, Seen, Picture, Category, Order, Abuse, Helpful, Review

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
        'Order': Order,
        'Abuse': Abuse,
        'Helpful': Helpful,
        'Review': Review
    }

