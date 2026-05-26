from flask import Flask, request, jsonify

app = Flask(__name__)

books_db = [
    {"id": 1, "title": "Война и мир", "author": "Лев Толстой", "price": 500},
    {"id": 2, "title": "Преступление и наказание", "author": "Фёдор Достоевский", "price": 350},
    {"id": 3, "title": "Мастер и Маргарита", "author": "Михаил Булгаков", "price": 420},
]

@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books_db), 200

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((b for b in books_db if b['id'] == book_id), None)
    if book:
        return jsonify(book), 200
    return jsonify({"error": "Книга не найдена"}), 404

@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    new_id = max(b['id'] for b in books_db) + 1 if books_db else 1
    new_book = {
        "id": new_id,
        "title": data.get('title', 'Без названия'),
        "author": data.get('author', 'Неизвестен'),
        "price": data.get('price', 0)
    }
    books_db.append(new_book)
    return jsonify(new_book), 201

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "service": "books-service"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
