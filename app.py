from flask import Flask, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

books = [
    {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
    {"id": 2, "title": "1984", "author": "George Orwell"},
    {"id": 2, "title": "1984", "author": "George Orwell"},
    {"id": 2, "title": "1984", "author": "George Orwell"},
    {"id": 2, "title": "1984", "author": "George Orwell"},
    {"id": 2, "title": "1984", "author": "George Orwell"},
    {"id": 2, "title": "1984", "author": "George Orwell"},
    {"id": 2, "title": "1984", "author": "George Orwell"},
    {"id": 2, "title": "1984", "author": "George Orwell"},
    {"id": 2, "title": "1984", "author": "George Orwell"},
    {"id": 2, "title": "1984", "author": "George Orwell"},
    {"id": 2, "title": "1984", "author": "George Orwell"},
    {"id": 2, "title": "1984", "author": "George Orwell"},
    {"id": 2, "title": "1984", "author": "George Orwell"},
    {"id": 2, "title": "1984", "author": "George Orwell"},
    {"id": 2, "title": "1984", "author": "George Orwell"},
    {"id": 2, "title": "1984", "author": "George Orwell"},
    {"id": 2, "title": "1984", "author": "George Orwell"},
    {"id": 2, "title": "1984", "author": "George Orwell"}
]
limiter = Limiter(app, key_func=get_remote_address)


def find_book_by_id(book_id):
    """ Blah blah function Blah """
    for book in books:
        if book['id'] == book_id:
            return book
    return None


def validate_book_data(data):
    if 'title' not in data or 'author' not in data:
        return False
    return True


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Not Found'}), 404


@app.errorhandler(405)
def method_not_allowed_error(error):
    return jsonify({'error': 'Method Not Allowed'}), 405


@app.route('/api/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = find_book_by_id(id)

    if book is None:
        return 'Oh fucking shit Homie!!', 404
    else:
        for index, book in enumerate(books):
            if book['id'] == id:
                del books[index]

    return jsonify(book)


@app.route('/api/books/<int:id>', methods=['PUT'])
def slap_a_book(id):
    book = find_book_by_id(id)

    if book is None:
        return 'We couldn`t find that fuckin book!', 404

    new_data = request.get_json()
    book.update(new_data)

    return jsonify(book)


@app.route('/api/books', methods=['GET', 'POST'])
@limiter.limit('10/minute')
def slap_books():
    """ This is a function.  This docstring is not written correctly. """
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))

    start_index = (page - 1) * limit
    end_index = start_index + limit

    paginated_books = books[start_index:end_index]
    author = request.args.get('author')

    if author:
        filtered_books = [book for book in books if book['author'] == author]
        return jsonify(filtered_books)

    if request.method == 'POST':
        new_book = request.get_json()

        if not validate_book_data(new_book):
            return jsonify({'error': 'Invalid book data'}), 400

        new_id = max(book['id'] for book in books) + 1
        new_book['id'] = new_id

        books.append(new_book)

        return jsonify(new_book), 201
    return jsonify(paginated_books)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
