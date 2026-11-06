import os
from flask import Flask, render_template, request, jsonify
import category as category_service
import product as product_service
import cart as cart_service
import shipping as shipping_service

app = Flask(__name__)

def seed_initial_data():
    if not category_service.get_all_categories():
        initial_categories = [
            (1, "Electronics"),
            (2, "Books"),
            (3, "Clothing"),
            (4, "Home & Lifestyle")
        ]
        for cat_id, cat_name in initial_categories:
            category_service.create_category(cat_id, cat_name)

        initial_products = [
            (101, "Wireless Mouse", 1, 799.00, 25),
            (102, "Mechanical Keyboard", 1, 2499.00, 15),
            (103, "USB-C Hub Multiport", 1, 1499.00, 20),
            (201, "Python Fundamentals", 2, 649.00, 30),
            (202, "Data Analytics Handbook", 2, 899.00, 18),
            (301, "Cotton Crewneck T-Shirt", 3, 599.00, 40),
            (302, "Performance Running Shoes", 3, 2199.00, 12),
            (401, "Insulated Water Bottle", 4, 449.00, 50)
        ]
        for p_id, p_name, c_id, price, stock in initial_products:
            product_service.create_product(p_id, p_name, c_id, price, stock)

seed_initial_data()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/categories", methods=["GET"])
def get_categories():
    try:
        categories = category_service.get_all_categories()
        return jsonify(categories)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/categories", methods=["POST"])
def add_category():
    try:
        data = request.get_json()
        category_id = int(data.get("category_id"))
        category_name = data.get("category_name")
        result = category_service.create_category(category_id, category_name)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/products", methods=["GET"])
def get_products():
    try:
        category_id = request.args.get("category_id")
        search_query = request.args.get("search")

        if search_query:
            products = product_service.search_products(search_query)
            if category_id:
                products = [p for p in products if str(p.get("category_id")) == str(category_id)]
        elif category_id:
            products = product_service.get_products_by_category(int(category_id))
        else:
            products = product_service.get_all_products()

        return jsonify(products)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/products", methods=["POST"])
def add_product():
    try:
        data = request.get_json()
        product_id = int(data.get("product_id"))
        product_name = data.get("product_name")
        category_id = int(data.get("category_id"))
        price = float(data.get("price"))
        stock = int(data.get("stock"))

        result = product_service.create_product(
            product_id=product_id,
            product_name=product_name,
            category_id=category_id,
            price=price,
            stock=stock
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/cart/<int:user_id>", methods=["GET"])
def get_cart(user_id):
    try:
        cart = cart_service.get_cart(user_id)
        return jsonify(cart)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/cart", methods=["POST"])
def add_to_cart():
    try:
        data = request.get_json()
        user_id = int(data.get("user_id"))
        product_id = int(data.get("product_id"))
        quantity = int(data.get("quantity", 1))

        result = cart_service.add_to_cart(user_id, product_id, quantity)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/cart", methods=["PUT"])
def update_cart():
    try:
        data = request.get_json()
        user_id = int(data.get("user_id"))
        product_id = int(data.get("product_id"))
        quantity = int(data.get("quantity"))

        result = cart_service.update_quantity(user_id, product_id, quantity)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/cart", methods=["DELETE"])
def remove_from_cart():
    try:
        data = request.get_json()
        user_id = int(data.get("user_id"))
        product_id = int(data.get("product_id"))

        result = cart_service.remove_from_cart(user_id, product_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/checkout", methods=["POST"])
def checkout():
    try:
        data = request.get_json()
        user_id = int(data.get("user_id"))

        cart = cart_service.get_cart(user_id)
        if not cart["items"]:
            return jsonify({"error": "Cart is empty."}), 400

        for item in cart["items"]:
            prod = product_service.get_product(item["product_id"])
            if int(item["quantity"]) > int(prod["stock"]):
                return jsonify({"error": f"Insufficient stock for {prod['product_name']}. Available: {prod['stock']}"}), 400

        reduced_items = []
        try:
            for item in cart["items"]:
                product_service.reduce_stock(item["product_id"], item["quantity"])
                reduced_items.append(item)
            shipping_details = shipping_service.create_shipping_details(cart["items"])
        except Exception as err:
            for item in reduced_items:
                product_service.restore_stock(item["product_id"], item["quantity"])
            raise err

        cart_service.clear_cart(user_id)

        return jsonify({
            "message": "Order placed successfully!",
            "shipping": shipping_details,
            "subtotal": cart["subtotal"]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
