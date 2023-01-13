import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, request, render_template, jsonify
from pymongo import MongoClient

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

client = MongoClient(os.environ.get('MONGODB_URI'))
db = client[os.environ.get('DB_NAME')]

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/mars', methods=['POST'])
def web_mars_post():
    name_receive = request.form['name_give']
    address_receive = request.form['address_give']
    size_receive = request.form['size_give']
    
    db.orders.insert_one({
        'name': name_receive,
        'address': address_receive,
        'size': size_receive
    })
    
    return jsonify({'msg': 'complete!'})

@app.route('/mars', methods=['GET'])
def web_mars_get():
    order_list = list(db.orders.find({}, {'_id': False}))
    return jsonify({
        'orders': order_list
    })

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
