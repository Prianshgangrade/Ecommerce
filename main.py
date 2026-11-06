import category as category_service
import product as product_service
import cart as cart_service
import shipping as shipping_service


def show_menu():
    print("    E-COMMERCE APPLICATION")
    print("1.  Add category")
    print("2.  View categories")
    print("3.  Add product")
    print("4.  View products")
    print("5.  Search product")
    print("6.  Add product to cart")
    print("7.  View cart")
    print("8.  Remove product from cart")
    print("9. Checkout")
    print("0.  Exit")

def add_category():
    print("\nAdd Category -")

    category_id = int(input("Enter category ID: "))
    category_name = input("Enter category name: ").strip()

    result = category_service.create_category(
        category_id=category_id,
        category_name=category_name
    )

    print(result["message"])


def view_categories():
    print("\n--- Categories ---")

    categories = category_service.get_all_categories()

    if not categories:
        print("No categories available.")
        return

    for category in categories:
        print(
            f"Category ID: {category['category_id']} | "
            f"Name: {category['category_name']}"
        )


def add_product():
    print("\n-Add Product ")

    categories = category_service.get_all_categories()

    if not categories:
        print("Please create a category first.")
        return

    print("\nAvailable categories:")

    for category in categories:
        print(
            f"{category['category_id']} - "
            f"{category['category_name']}"
        )

    product_id = int(input("\nEnter product ID: "))
    product_name = input("Enter product name: ").strip()
    category_id = int(input("Enter category ID: "))
    price = float(input("Enter product price: "))
    stock = int(input("Enter available stock: "))

    result = product_service.create_product(
        product_id=product_id,
        product_name=product_name,
        category_id=category_id,
        price=price,
        stock=stock
    )

    print(result["message"])


def view_products():
    print("\n--- Products ---")

    products = product_service.get_all_products()

    if not products:
        print("No products available.")
        return

    for product in products:
        print(f"Product ID : {product['product_id']}")
        print(f"Name       : {product['product_name']}")
        print(f"Category   : {product['category_name']}")
        print(f"Price      : Rs. {float(product['price']):.2f}")
        print(f"Stock      : {product['stock']}")


def search_product():
    print("\n--- Search Product ---")

    search_text = input("Enter product name to search: ").strip()

    products = product_service.search_products(search_text)

    if not products:
        print("No matching products found.")
        return

    for product in products:
        print(f"Product ID : {product['product_id']}")
        print(f"Name       : {product['product_name']}")
        print(f"Price      : Rs. {float(product['price']):.2f}")
        print(f"Stock      : {product['stock']}")

def add_product_to_cart():
    print("\n--- Add Product to Cart ---")

    products = product_service.get_all_products()

    if not products:
        print("No products are available.")
        return

    print("\nAvailable products:")

    for product in products:
        print(
            f"ID: {product['product_id']} | "
            f"Name: {product['product_name']} | "
            f"Price: Rs. {float(product['price']):.2f} | "
            f"Stock: {product['stock']}"
        )

    user_id = int(input("\nEnter user ID: "))
    product_id = int(input("Enter product ID: "))
    quantity = int(input("Enter quantity: "))

    result = cart_service.add_to_cart(
        user_id=user_id,
        product_id=product_id,
        quantity=quantity
    )

    print(result["message"])


def view_cart():
    print("\nView Cart")

    user_id = int(input("Enter user ID: "))

    cart = cart_service.get_cart(user_id)

    if not cart["items"]:
        print("The cart is empty.")
        return

    print(f"\nCart for user {user_id}:")

    for item in cart["items"]:
        print(f"Product ID : {item['product_id']}")
        print(f"Name       : {item['product_name']}")
        print(f"Quantity   : {item['quantity']}")
        print(f"Unit Price : Rs. {float(item['unit_price']):.2f}")
        print(f"Line Total : Rs. {float(item['line_total']):.2f}")

    print(f"Subtotal   : Rs. {float(cart['subtotal']):.2f}")


def update_cart_quantity():
    print("\n--- Update Cart Quantity ---")

    user_id = int(input("Enter user ID: "))
    product_id = int(input("Enter product ID: "))
    quantity = int(input("Enter new quantity: "))

    result = cart_service.update_quantity(
        user_id=user_id,
        product_id=product_id,
        quantity=quantity
    )

    print(result["message"])


def remove_cart_item():
    print("\n-Remove Product from Cart")

    user_id = int(input("Enter user ID: "))
    product_id = int(input("Enter product ID: "))

    result = cart_service.remove_from_cart(
        user_id=user_id,
        product_id=product_id
    )

    print(result["message"])


def checkout():
    print("\n--- Checkout ---")

    user_id = int(input("Enter user ID: "))

    cart = cart_service.get_cart(user_id)

    if not cart["items"]:
        print("The cart is empty.")
        return
    for item in cart["items"]:
        product = product_service.get_product(
            item["product_id"]
        )

        available_stock = int(product["stock"])
        requested_quantity = int(item["quantity"])

        if requested_quantity > available_stock:
            raise ValueError(
                f"Insufficient stock for "
                f"{product['product_name']}. "
                f"Available stock: {available_stock}"
            )

    reduced_items = []

    try:
        for item in cart["items"]:
            product_service.reduce_stock(
                product_id=item["product_id"],
                quantity=item["quantity"]
            )

            reduced_items.append(item)
        shipping_details = (
            shipping_service.create_shipping_details(
                cart["items"]
            )
        )

    except Exception:
        for item in reduced_items:
            product_service.restore_stock(
                product_id=item["product_id"],
                quantity=item["quantity"]
            )

        raise


    print(" ORDER PLACED")


    print("\nProducts for delivery:")

    for product in shipping_details["products"]:
        print(f"Product ID   : {product['product_id']}")
        print(f"Product name : {product['product_name']}")
        print(f"Quantity     : {product['quantity']}")

    print(
        f"Delivery time: "
        f"{shipping_details['delivery_time']}"
    )
    cart_service.clear_cart(user_id)

def main():
    while True:
        show_menu()

        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                add_category()

            elif choice == "2":
                view_categories()

            elif choice == "3":
                add_product()

            elif choice == "4":
                view_products()

            elif choice == "5":
                search_product()

            elif choice == "6":
                add_product_to_cart()

            elif choice == "7":
                view_cart()

            elif choice == "8":
                remove_cart_item()

            elif choice == "9":
                checkout()

            elif choice == "0":
                print("\nApplication closed.")
                break

            else:
                print(
                    "\nInvalid choice. "
                    "Please choose a number from 0 to 10."
                )

        except ValueError as error:
            print(f"\nError: {error}")

        except Exception as error:
            print(f"\nUnexpected error: {error}")


if __name__ == "__main__":
    # print("yes")
    main()