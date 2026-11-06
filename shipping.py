import random


def create_shipping_details(cart_items):
    if not cart_items:
        raise ValueError(
            "Cannot create shipping details for an empty cart."
        )

    products = []

    for item in cart_items:
        products.append({
            "product_id": int(item["product_id"]),
            "product_name": str(item["product_name"]),
            "quantity": int(item["quantity"])
        })

    delivery_days = random.randint(2, 5)

    return {
        "products": products,
        "delivery_time": f"{delivery_days} working days"
    }