from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

BOOKS_SERVICE_URL = os.environ.get('BOOKS_SERVICE_URL', 'http://localhost:5001')

orders_db = []
order_counter = 1

@app.route('/orders', methods=['POST'])
def create_order():
    global order_counter
    data = request.get_json()
    book_id = data.get('book_id')
    quantity = data.get('quantity', 1)

    try:
        resp = requests.get(f'{BOOKS_SERVICE_URL}/books/{book_id}', timeout=5)
        if resp.status_code != 200:
            return jsonify({'error': 'Книга не найдена в каталоге'}), 404
        book = resp.json()
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Не удалось связаться с books-service: {str(e)}'}), 503

    new_order = {
        'order_id': order_counter,
        'book': book,
        'quantity': quantity,
        'total_price': book['price'] * quantity,
        'status': 'created'
    }
    orders_db.append(new_order)
    order_counter += 1
    return jsonify(new_order), 201

@app.route('/orders', methods=['GET'])
def get_orders():
    return jsonify(orders_db), 200

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = next((o for o in orders_db if o['order_id'] == order_id), None)
    if order:
        return jsonify(order), 200
    return jsonify({'error': 'Заказ не найден'}), 404

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'service': 'orders-service'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
