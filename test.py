from flask import Flask, jsonify, request

app = Flask(__name__)

books = [
    {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
    {"id": 2, "title": "1984", "author": "George Orwell"}
]


def find_book_by_id(book_id):
    """ Blah blah function Blah """
    for book in books:
        if book['id'] == book_id:
            return book
        else:
            return None


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
def slap_books():
    """ This is a function """
    if request.method == 'POST':
        new_book = request.get_json()

        new_id = max(book['id'] for book in books) + 1
        new_book['id'] = new_id

        books.append(new_book)

        return jsonify(new_book), 201
    else:
        return jsonify(books)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
