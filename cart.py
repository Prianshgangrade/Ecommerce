import pandas as pd
import numpy as np

import product as product_service


# Empty DataFrame used to store cart items.
cart_df = pd.DataFrame(
    columns=[
        "user_id",
        "product_id",
        "product_name",
        "quantity",
        "unit_price",
        "line_total"
    ]
)


def add_to_cart(user_id, product_id, quantity):
    global cart_df

    user_id = int(user_id)
    product_id = int(product_id)
    quantity = int(quantity)

    if quantity <= 0:
        raise ValueError(
            "Quantity must be greater than zero."
        )

    # Get product details from product_service.py.
    product = product_service.get_product(product_id)

    available_stock = int(product["stock"])
    unit_price = float(product["price"])

    # Find this product in this user's cart.
    existing_mask = (
        (cart_df["user_id"] == user_id)
        & (cart_df["product_id"] == product_id)
    )

    existing_quantity = 0

    if existing_mask.any():
        existing_quantity = int(
            cart_df.loc[
                existing_mask,
                "quantity"
            ].iloc[0]
        )

    total_quantity = existing_quantity + quantity

    # Cart quantity cannot be greater than product stock.
    if total_quantity > available_stock:
        raise ValueError(
            f"Only {available_stock} units are available."
        )

    # If product is already present, update its quantity.
    if existing_mask.any():
        cart_df.loc[
            existing_mask,
            "quantity"
        ] = total_quantity

        cart_df.loc[
            existing_mask,
            "unit_price"
        ] = unit_price

        cart_df.loc[
            existing_mask,
            "line_total"
        ] = np.round(
            total_quantity * unit_price,
            2
        )

    # Otherwise, add a new row to the cart.
    else:
        new_item = pd.DataFrame([
            {
                "user_id": user_id,
                "product_id": product_id,
                "product_name": product["product_name"],
                "quantity": quantity,
                "unit_price": unit_price,
                "line_total": np.round(
                    quantity * unit_price,
                    2
                )
            }
        ])

        cart_df = pd.concat(
            [cart_df, new_item],
            ignore_index=True
        )

    return {
        "message": "Product added to cart successfully."
    }


def get_cart(user_id):
    user_id = int(user_id)

    # Select only the rows belonging to this user.
    user_cart = cart_df[
        cart_df["user_id"] == user_id
    ].copy()

    if user_cart.empty:
        subtotal = 0.0
    else:
        subtotal = float(
            user_cart["line_total"].sum()
        )

    return {
        "user_id": user_id,
        "items": user_cart.to_dict(
            orient="records"
        ),
        "subtotal": round(subtotal, 2)
    }


def update_quantity(user_id, product_id, quantity):
    global cart_df

    user_id = int(user_id)
    product_id = int(product_id)
    quantity = int(quantity)

    # A quantity of zero removes the product.
    if quantity == 0:
        return remove_from_cart(
            user_id,
            product_id
        )

    if quantity < 0:
        raise ValueError(
            "Quantity cannot be negative."
        )

    # Find the product in this user's cart.
    mask = (
        (cart_df["user_id"] == user_id)
        & (cart_df["product_id"] == product_id)
    )

    if not mask.any():
        raise ValueError(
            "Product is not present in the cart."
        )

    # Get the latest price and stock.
    product = product_service.get_product(product_id)

    available_stock = int(product["stock"])
    unit_price = float(product["price"])

    if quantity > available_stock:
        raise ValueError(
            f"Only {available_stock} units are available."
        )

    # Update the exact quantity.
    cart_df.loc[
        mask,
        "quantity"
    ] = quantity

    cart_df.loc[
        mask,
        "unit_price"
    ] = unit_price

    cart_df.loc[
        mask,
        "line_total"
    ] = np.round(
        quantity * unit_price,
        2
    )

    return {
        "message": "Cart quantity updated successfully."
    }


def remove_from_cart(user_id, product_id):
    global cart_df

    user_id = int(user_id)
    product_id = int(product_id)

    # Find the product in this user's cart.
    mask = (
        (cart_df["user_id"] == user_id)
        & (cart_df["product_id"] == product_id)
    )

    if not mask.any():
        raise ValueError(
            "Product is not present in the cart."
        )

    # Keep every row except the matching row.
    cart_df = cart_df[
        ~mask
    ].reset_index(drop=True)

    return {
        "message": "Product removed from cart successfully."
    }


def clear_cart(user_id):
    global cart_df

    user_id = int(user_id)

    # Remove all cart items belonging to the user.
    cart_df = cart_df[
        cart_df["user_id"] != user_id
    ].reset_index(drop=True)

    return {
        "message": "Cart cleared successfully."
    }