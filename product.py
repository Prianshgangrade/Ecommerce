import pandas as pd
import numpy as np

import  category as category_service 


products_df = pd.DataFrame(
    columns=[
        "product_id",
        "product_name",
        "category_id",
        "price",
        "stock"
    ]
)


def create_product(
    product_id,
    product_name,
    category_id,
    price,
    stock
):
    global products_df

    product_id = int(product_id)
    product_name = str(product_name).strip()
    category_id = int(category_id)
    price = float(price)
    stock = int(stock)

    if product_id in products_df["product_id"].values:
        raise ValueError("Product ID already exists.")

    if not product_name:
        raise ValueError("Product name cannot be empty.")

    if not category_service.category_exists(category_id):
        raise ValueError("Category does not exist.")

    if price <= 0:
        raise ValueError("Price must be greater than zero.")

    if stock < 0:
        raise ValueError("Stock cannot be negative.")

    new_product = pd.DataFrame([
        {
            "product_id": product_id,
            "product_name": product_name,
            "category_id": category_id,
            "price": np.round(price, 2),
            "stock": stock
        }
    ])

    products_df = pd.concat(
        [products_df, new_product],
        ignore_index=True
    )

    return {
        "message": "Product created successfully.",
        "product_id": product_id
    }


def get_product(product_id):
    product_id = int(product_id)

    result = products_df[
        products_df["product_id"] == product_id
    ]

    if result.empty:
        raise ValueError("Product not found.")

    return result.iloc[0].to_dict()


def get_all_products():
    if products_df.empty:
        return []

    result = products_df.merge(
        category_service.categories_df,
        on="category_id",
        how="left"
    )

    return result.to_dict(orient="records")


def get_products_by_category(category_id):
    category_id = int(category_id)

    result = products_df[
        products_df["category_id"] == category_id
    ]

    return result.to_dict(orient="records")


def search_products(search_text):
    search_text = str(search_text).strip()

    result = products_df[
        products_df["product_name"].str.contains(
            search_text,
            case=False,
            na=False
        )
    ]

    return result.to_dict(orient="records")


def update_product(
    product_id,
    product_name=None,
    price=None,
    stock=None
):
    global products_df

    product_id = int(product_id)

    mask = products_df["product_id"] == product_id

    if not mask.any():
        raise ValueError("Product not found.")

    if product_name is not None:
        product_name = str(product_name).strip()

        if not product_name:
            raise ValueError("Product name cannot be empty.")

        products_df.loc[
            mask,
            "product_name"
        ] = product_name

    if price is not None:
        price = float(price)

        if price <= 0:
            raise ValueError(
                "Price must be greater than zero."
            )

        products_df.loc[
            mask,
            "price"
        ] = np.round(price, 2)

    if stock is not None:
        stock = int(stock)

        if stock < 0:
            raise ValueError("Stock cannot be negative.")

        products_df.loc[mask, "stock"] = stock

    return {
        "message": "Product updated successfully."
    }


def delete_product(product_id):
    global products_df

    product_id = int(product_id)

    mask = products_df["product_id"] == product_id

    if not mask.any():
        raise ValueError("Product not found.")

    products_df = products_df[
        ~mask
    ].reset_index(drop=True)

    return {
        "message": "Product deleted successfully."
    }


def reduce_stock(product_id, quantity):
    global products_df

    product_id = int(product_id)
    quantity = int(quantity)

    if quantity <= 0:
        raise ValueError(
            "Quantity must be greater than zero."
        )

    mask = products_df["product_id"] == product_id

    if not mask.any():
        raise ValueError("Product not found.")

    current_stock = int(
        products_df.loc[mask, "stock"].iloc[0]
    )

    if current_stock < quantity:
        raise ValueError(
            f"Insufficient stock. "
            f"Available stock: {current_stock}"
        )

    products_df.loc[
        mask,
        "stock"
    ] = current_stock - quantity


def restore_stock(product_id, quantity):
    global products_df

    product_id = int(product_id)
    quantity = int(quantity)

    if quantity <= 0:
        raise ValueError(
            "Quantity must be greater than zero."
        )

    mask = products_df["product_id"] == product_id

    if not mask.any():
        raise ValueError("Product not found.")

    current_stock = int(
        products_df.loc[mask, "stock"].iloc[0]
    )

    products_df.loc[
        mask,
        "stock"
    ] = current_stock + quantity