# Tallie
## Your best e-commerce for books and more

Tallie is a e-commerce especially created for books with built-in review analysis to help you pick up your next book.

## Feature
- Search for books by names, categories or sellers.
- Featuring best-selling books, most-viewed books, etc. to find out what's trending.
- Full support on buying and selling process.
- Apply machine learning to support sentiment analysis.
- Real-time tracking ordering process.

## Tech

Tallie uses a number of framework in the following:
- Flask
- Flask-SQLAlchemy
- Flask-HTTPAuth
- Jinja2
- Elasticsearch
- PostgreSQL
- Twitter Bootstrap
- jQuery
- Draft.js - Facebook's lightweight text editor

## Installation

Tallie requires Python 3.9+ to run.

```sh
cd tallie-backend
```

Accessing virtual environment
- On Windows
```sh
.\venv\Scripts\activate
```

- On MacOS or Linux
```sh
source venv\bin\activate
```

Install require packages and run the server.
```sh
pip install -r requirements.txt
flask run
```