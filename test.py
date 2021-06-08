from datetime import datetime
from app import db
from app.models import User, Product, Payment, Wishlist, Seen, Picture, Category, Abuse, Helpful, Review

def test(product_id, img_id):
    picture = Picture(product_id=product_id, img_id=img_id)
    db.session.add(picture)
    db.session.commit()
    product = Product.query.filter_by(id=product_id).first()
    product.pictures.append(picture)
    db.session.add(product)
    db.session.commit()

# test(product_id=15, img_id=21)