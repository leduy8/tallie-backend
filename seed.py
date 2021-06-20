from datetime import datetime
from app import db
from app.models import User, Product, Payment, Wishlist, Seen, Picture, Category, Abuse, Helpful, Review
from tallie_app import app


def create_all():
    with app.app_context():
        create_all_categories()
        create_base_user()
        create_all_product()
        create_reviews()


def create_all_categories():
    business_money = Category(name='Business & Money')
    children = Category(name='Children\'s book')
    technology = Category(name='Computers & Technology')
    cookbook = Category(name='Cookbook')
    hobbies = Category(name='Hobbies')
    edu = Category(name='Education & Teaching')
    health = Category(name='Health, Fitness & Dieting')
    history = Category(name='History')
    entertain = Category(name='Humor & Entertainment')
    law = Category(name='Law')
    literature_fiction = Category(name='Literature & Fiction')
    medical = Category(name='Medical Books')
    mystery_thriller = Category(name='Mystery & Thriller')
    parent_relationship = Category(name='Parenting & Relationships')
    politics_social = Category(name='Politics & Social Sciences')
    romance = Category(name='Romance')
    science_math = Category(name='Science & Math')
    scifi_fantasy = Category(name='Science Fiction & Fantasy')
    selfhelp = Category(name='Self-Help')
    sports = Category(name='Sports & Outdoors')
    teen = Category(name='Teen & Young Adult')
    travel = Category(name='Travel')
    db.session.add(business_money)
    db.session.add(children)
    db.session.add(technology)
    db.session.add(cookbook)
    db.session.add(hobbies)
    db.session.add(edu)
    db.session.commit()
    db.session.add(health)
    db.session.add(history)
    db.session.add(entertain)
    db.session.add(law)
    db.session.add(literature_fiction)
    db.session.add(medical)
    db.session.add(mystery_thriller)
    db.session.commit()
    db.session.add(parent_relationship)
    db.session.add(politics_social)
    db.session.add(romance)
    db.session.add(science_math)
    db.session.add(scifi_fantasy)
    db.session.add(selfhelp)
    db.session.commit()
    db.session.add(sports)
    db.session.add(teen)
    db.session.add(travel)
    db.session.commit()


def create_base_user():
    # seller = User(username='duy123', name='Le Duc Duy', email='fantasyboi8@gmail.com', phone='0987654321',
    #               address='121 Thai Ha, Thanh Xuan, Ha Noi', bio='This is a very very very very very very very long text!', is_seller=True)
    buyer1 = User(username='buyer007', name='James Bond', email='james_bond_007@gmail.com', phone='0987654322',
                  address='127 Thai Thinh, Thanh Xuan, Ha Noi', bio='This is a very very very very very very very long text!')
    buyer2 = User(username='messi10', name='Lionel Messi', email='messi10@gmail.com', phone='0987654323', address='128 Thai Thinh, Thanh Xuan, Ha Noi',
                  bio='This is a very very very very very very very long text and messi number 1!')
    buyer3 = User(username='ronaldo7', name='Cristiano Ronaldo', email='ronaldo7@gmail.com', phone='0987654324', address='129 Thai Thinh, Thanh Xuan, Ha Noi',
                  bio='This is a very very very very very very very long text and ronaldo number 1!')
    # seller.set_password('123456')
    buyer1.set_password('123456')
    buyer2.set_password('123456')
    buyer3.set_password('123456')
    # db.session.add(seller)
    db.session.add(buyer1)
    db.session.add(buyer2)
    db.session.add(buyer3)
    db.session.commit()


def create_all_product():
    # ? [Business & Money = 0, Children's book = 1, Computers & Technology = 2, Cookbook = 3, Hobbies = 4, Education & Teaching = 5, Health Fitness & Dieting = 6, History = 7, Humor & Entertainment = 8, Law = 9, Literature & Fiction = 10, Medical Books = 11, Mystery & Thriller = 12, Parenting & Relationships = 13, Politics & Social Sciences = 14, Romance = 15, Science & Math = 16, Science Fiction & Fantasy = 17, Self-Help = 18, Sports & Outdoors = 19, Teen & Young Adult = 20, Travel = 21]
    category_list = Category.query.all()
    product_1 = Product(name='The Chronicles of Narnia', author='C. S. Lewis', price='150000',
                        description='The Chronicles of Narnia is a series of seven fantasy novels by British author C. S. Lewis. Illustrated by Pauline Baynes and originally published between 1950 and 1956, The Chronicles of Narnia has been adapted for radio, television, the stage, film and computer games. The series is set in the fictional realm of Narnia, a fantasy world of magic, mythical beasts and talking animals. It narrates the adventures of various children who play central roles in the unfolding history of the Narnian world. Except in The Horse and His Boy, the protagonists are all children from the real world who are magically transported to Narnia, where they are sometimes called upon by the lion Aslan to protect Narnia from evil. The books span the entire history of Narnia, from its creation in The Magician\'s Nephew to its eventual destruction in The Last Battle.', quantity=6, seller_id=1, categories=[category_list[10]])
    product_2 = Product(name='Pride and Prejudice', author='Jane Austen', price='90000',
                        description='Few have failed to be charmed by the witty and independent spirit of Elizabeth Bennet in Austen’s beloved classic Pride and Prejudice. When Elizabeth Bennet first meets eligible bachelor Fitzwilliam Darcy, she thinks him arrogant and conceited; he is indifferent to her good looks and lively mind. When she later discovers that Darcy has involved himself in the troubled relationship between his friend Bingley and her beloved sister Jane, she is determined to dislike him more than ever. In the sparkling comedy of manners that follows, Jane Austen shows us the folly of judging by first impressions and superbly evokes the friendships, gossip and snobberies of provincial middle-class life.', quantity=10, seller_id=1, categories=[category_list[10]])
    product_3 = Product(name='Start with Why: How Great Leaders Inspire Everyone to Take Action', author='Simon Sinek', price='120000',
                        description='Start with Why shows that the leaders who\'ve had the greatest influence in the world all think, act, and communicate the same way - and it\'s the opposite of what everyone else does. Sinek calls this powerful idea The Golden Circle, and it provides a framework upon which organizations can be built, movements can be led, and people can be inspired. And it all starts with why.', quantity=3, seller_id=1, categories=[category_list[18]])
    product_4 = Product(name='Elon Musk: Tesla, SpaceX, and the Quest for a Fantastic Future', author='Ashlee Vance', price='290000',
                        description='In the spirit of Steve Jobs and Moneyball, Elon Musk is both an illuminating and authorized look at the extraordinary life of one of Silicon Valley\'s most exciting, unpredictable, and ambitious entrepreneurs - a real-life Tony Stark - and a fascinating exploration of the renewal of American invention and its new makers. Elon Musk spotlights the technology and vision of Elon Musk, the renowned entrepreneur and innovator behind SpaceX, Tesla, and SolarCity, who sold one of his Internet companies, PayPal, for $1.5 billion. Ashlee Vance captures the full spectacle and arc of the genius\' life and work, from his tumultuous upbringing in South Africa and flight to the United States to his dramatic technical innovations and entrepreneurial pursuits. Vance uses Musk\'s story to explore one of the pressing questions of our age: Can the nation of inventors and creators who led the modern world for a century still compete in an age of fierce global competition? He argues that Musk - one of the most unusual and striking figures in American business history - is a contemporary, visionary amalgam of legendary inventors and industrialists, including Thomas Edison, Henry Ford, Howard Hughes, and Steve Jobs. More than any other entrepreneur today, Musk has dedicated his energies and his own vast fortune to inventing a future that is as rich and far reaching as the visionaries of the golden age of science-fiction fantasy.', quantity=2, seller_id=1, categories=[category_list[7]])
    product_5 = Product(name='Steve Jobs', author='Walter Isaacson', price='450000',
                        description='Based on more than 40 interviews with Jobs conducted over two years - as well as interviews with more than a hundred family members, friends, adversaries, competitors, and colleagues - Walter Isaacson has written a riveting story of the roller-coaster life and searingly intense personality of a creative entrepreneur whose passion for perfection and ferocious drive revolutionized six industries: personal computers, animated movies, music, phones, tablet computing, and digital publishing. At a time when America is seeking ways to sustain its innovative edge, and when societies around the world are trying to build digital-age economies, Jobs stands as the ultimate icon of inventiveness and applied imagination. He knew that the best way to create value in the 21st century was to connect creativity with technology. He built a company where leaps of the imagination were combined with remarkable feats of engineering. Although Jobs cooperated with this book, he asked for no control over what was written. He put nothing off-limits. He encouraged the people he knew to speak honestly. And Jobs speaks candidly, sometimes brutally so, about the people he worked with and competed against. His friends, foes, and colleagues provide an unvarnished view of the passions, perfectionism, obsessions, artistry, devilry, and compulsion for control that shaped his approach to business and the innovative products that resulted. Driven by demons, Jobs could drive those around him to fury and despair. But his personality and products were interrelated, just as Apple\'s hardware and software tended to be, as if part of an integrated system. His tale is instructive and cautionary, filled with lessons about innovation, character, leadership, and values.', quantity=1, seller_id=1, categories=[category_list[7]])
    product_6 = Product(name='The Art of War', author='Sun Tzu', price='150000',
                        description='The 13 chapters of The Art of War, each devoted to one aspect of warfare, were compiled by the high-ranking Chinese military general, strategist, and philosopher Sun-Tzu. In spite of its battlefield specificity, The Art of War has found new life in the modern age, with leaders in fields as wide and far-reaching as world politics, human psychology, and corporate strategy finding valuable insight in its timeworn words. Aidan Gillen - who has learned a thing or two about strategy through his roles as skilled manipulator Petyr "Littlefinger" Baelish (Game of Thrones) and ambitious politician Tommy Carcetti (The Wire) - brilliantly performs this ancient classic. His experience in portraying insightful and, at times, cunning characters makes him a natural fit for this ancient collection of battlefield epigrams whose influence has grown tremendously in the modern world.', quantity=12, seller_id=1, categories=[category_list[7]])
    product_7 = Product(name='Symposium', author='Plato', price='130000',
                        description='The dramatic nature of Plato\'s dialogues is delightfully evident in Symposium. The marriage between character and thought bursts forth as the guests gather at Agathon\'s house to celebrate the success of his first tragedy. With wit and insight, they all present their ideas about love - from Erixymachus\' scientific naturalism to Aristophanes\' comic fantasy. The unexpected arrival of Alcibiades breaks the spell cast by Diotima\'s ethereal climb up the staircase of love to beauty itself. Ecstasy and intoxication clash as Plato concludes with one of his most skillful displays of dialectic.', quantity=9, seller_id=1, categories=[category_list[14]])
    product_8 = Product(name='Discourses and Selected Writings', author='Epictetus', price='100000',
                        description='DESPITE BEING BORN into slavery, Greco-Roman philosopher Epictetus became one of the most influential thinkers of his time. Discourses and Selected Writings is a transcribed collection of informal lectures given by the philosopher around AD 108. A gateway into the life and mind of a great intellectual, it is also an important example of the usage of Koine or ?common? Greek, an ancestor to Standard Modern Greek.', quantity=10, seller_id=1, categories=[category_list[14]])
    db.session.add(product_1)
    db.session.add(product_2)
    db.session.add(product_3)
    db.session.add(product_4)
    db.session.add(product_5)
    db.session.add(product_6)
    db.session.add(product_7)
    db.session.add(product_8)
    db.session.commit()


def create_reviews():
    buyer_1 = User.query.filter_by(username='buyer007').first()
    buyer_2 = User.query.filter_by(username='messi10').first()
    buyer_3 = User.query.filter_by(username='ronaldo7').first()
    product = Product.query.all()[0]
    product_2 = Product.query.all()[1]
    review_buyer_1 = Review(user_id=buyer_1.id, product_id=product.id, star=5, overview='Very good', content='I can\'t express how I love this book. It\'s like re-live childhood again.', prevent_spoiler=False, started_reading=datetime(2021, 1, 1), finished_reading=datetime(2021, 3, 1))
    review_buyer_2 = Review(user_id=buyer_2.id, product_id=product.id, star=4, overview='Good', content='Decent book, I will let my boy read this!.', prevent_spoiler=False, started_reading=datetime(2021, 3, 12), finished_reading=datetime(2021, 4, 8))
    review_buyer_3 = Review(user_id=buyer_3.id, product_id=product.id, star=4, overview='Very good', content='Aslan don\'t die noooo', prevent_spoiler=True)
    review_buyer_4 = Review(user_id=buyer_3.id, product_id=product_2.id, star=4, overview='Very good', content='Very good book tho')
    db.session.add(review_buyer_1)
    db.session.add(review_buyer_2)
    db.session.add(review_buyer_3)
    db.session.add(review_buyer_4)
    db.session.commit()


create_all()
