from flask import Flask, request, jsonify
import sqlite3
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATABASE = './main.db'

def initDB():
    if os.path.isfile(DATABASE):
        db = sqlite3.connect(DATABASE)
    else:
        with open('schema.sql', 'r') as file:
            sql_statements = file.read()

        db = sqlite3.connect(DATABASE)
        cursor = db.cursor()
        cursor.executescript(sql_statements)
        db.commit()
        db.close()

@app.route('/')
def hello():
    return 'Hello, Flask!'

@app.route('/order', methods=['POST'])
def process_data():
    data = request.get_json()
    
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute("SELECT id from `shops` WHERE address=?", (data['from'], ))
    shop_id = cursor.fetchone()[0]

    filter = []
    params = []
    for product in data['products']:
        product_id = product['product_id']
        filter.append('?')
        params.append(product_id)
    filter_str = ', '.join(filter)
    query = "SELECT id, price FROM products WHERE id IN ({})".format(filter_str)
    cursor.execute(query, params)
    prices = cursor.fetchall()

    amount = 0
    for index, product in enumerate(data['products']):
        count = int(product['count'])
        amount += count * int(prices[index][1])

    cursor.execute('INSERT INTO "orders"("id","shop_id","client_addr","amount") VALUES (NULL,?,NULL,?);', (shop_id, amount))
    order_id = cursor.lastrowid

    for index, product in enumerate(data['products']):
        product_id = product['product_id']
        count = int(product['count'])
        cursor.execute('INSERT INTO "order_products"("id","order_id","product_id","count") VALUES (NULL,?,?,?);', (order_id, product_id, count))

    db.commit()
    db.close()

    return str(order_id)

@app.route('/order/<id>', methods=['GET'])
def get_order(id):
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    
    ans = {}

    # products
    cursor.execute("SELECT  `name`, `price`, `count` FROM `order_products`, `products` \
                   WHERE `order_products`.`order_id`=? and `order_products`.`product_id`=`products`.`id`", (id, ))
    products = cursor.fetchall()

    ans['products'] = []
    for product in products:
        ans['products'].append({
            'name': product[0],
            'price': str(product[1]),
            'count': product[2]
        })

    # shop name
    cursor.execute("SELECT `address`, `name`, `amount`, `client_addr` FROM `shops`, `orders` WHERE `orders`.`shop_id`=`shops`.`id` and `orders`.`id`= ?", (id, ))
    result = cursor.fetchone()
    ans['shop'] = {
        'name': result[1],
        'address': result[0]
    }
    ans['amount'] = str(result[2])
    ans['client'] = result[3]

    return jsonify(ans)

@app.route('/order/<id>', methods=['PATCH'])
def update_client(id):
    client = request.get_json()['client']

    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    
    ans = {}

    # products
    cursor.execute("UPDATE `orders` SET `client_addr`=? WHERE `id`=?", (client, id ))

    db.commit()
    db.close()

    return jsonify({'status': 'OK'})


@app.route('/shop/check', methods=['POST'])
def shop_check():
    address = request.get_json()['address']
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM `shops` WHERE `address`=?", (address, ))
    result = cursor.fetchone()[0]
    print(result, type(result))
    if result != 0:
        return jsonify({'status': True})
    else:
        return jsonify({'status': False})

@app.route('/shop/<address>/products', methods=['GET'])
def shop_products(address):
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute("SELECT  `products`.`id`, `products`.`name`, `products`.`price`, `products`.`code` FROM `shops`, `products` \
                   WHERE `shops`.id = `products`.`shop_id`and `shops`.`address`=?", (address, ))
    result = cursor.fetchall()
    
    ans = {'products': {}}
    for product in result:
        ans['products'][str(product[3])] = {
            'id': product[0],
            'name': product[1],
            'price': str(product[2]),
        }
    return jsonify(ans)

if __name__ == '__main__':
    initDB()
    app.run(host="0.0.0.0")
