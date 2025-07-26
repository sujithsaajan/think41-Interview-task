from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load all datasets
def load_data():
    data = {}
    try:
        data['orders'] = pd.read_csv('data/orders.csv')
        data['products'] = pd.read_csv('data/products.csv')
        data['inventory'] = pd.read_csv('data/inventory_items.csv')
        print("✅ Data loaded successfully!")
        return data
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return None

data = load_data()

@app.route('/api/query', methods=['POST'])
def handle_query():
    query = request.json.get('query', '').lower()
    response = {"answer": "I couldn't process your request. Please try again."}

    # 1. Top products query
    if 'top' in query and ('product' in query or 'sold' in query):
        try:
            top_products = data['products'].nlargest(5, 'retail_price')[['name', 'retail_price']]
            response['answer'] = "Top 5 Products by Price:\n" + top_products.to_string(index=False)
        except Exception as e:
            response['answer'] = f"Error: {str(e)}"

    # 2. Order status query
    elif 'status' in query and 'order' in query:
        try:
            order_id = next((int(word) for word in query.split() if word.isdigit()), None)
            if order_id:
                status = data['orders'][data['orders']['order_id'] == order_id]['status'].values[0]
                response['answer'] = f"Order {order_id} status: {status}"
            else:
                response['answer'] = "Please specify an order ID."
        except:
            response['answer'] = "Order not found."

    # 3. Stock check query
    elif 'stock' in query or 'left' in query:
        try:
            product_name = next((name for name in data['products']['name'].unique() 
                               if name.lower() in query), None)
            if product_name:
                in_stock = data['inventory'][data['inventory']['product_name'] == product_name].shape[0]
                response['answer'] = f"Stock left for {product_name}: {in_stock}"
            else:
                response['answer'] = "Product not found."
        except Exception as e:
            response['answer'] = f"Error: {str(e)}"

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)