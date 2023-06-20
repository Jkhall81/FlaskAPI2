from flask import Flask, jsonify, request


app = Flask(__name__)


@app.route('/api/books', methods=['GET', 'POST'])
def books():
    """ This is a function! """
    books = [
        {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
        {"id": 2, "title": "1984", "author": "George Orwell"}
    ]
    if request.method == 'GET':

        return jsonify(books)

    elif request.method == 'POST':
        # Handle the POST request
        new_book = request.get_json()
        books.append(new_book)
        return jsonify(new_book), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
