from app import create_app, db
from app.models import User, Product, Payment, Wishlist, Seen, Picture, Avatar, Category, Abuse, Helpful, Review, ProductCategory

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


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
        'Avatar': Avatar,
        'Category': Category,
        'Abuse': Abuse,
        'Helpful': Helpful,
        'Review': Review,
        'ProductCategory': ProductCategory
    }
