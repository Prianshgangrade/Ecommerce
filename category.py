import pandas as pd


categories_df = pd.DataFrame(
    columns=[
        "category_id",
        "category_name"
    ]
)


def create_category(category_id, category_name):
    global categories_df

    category_id = int(category_id)
    category_name = str(category_name).strip()

    if not category_name:
        raise ValueError("Category name cannot be empty.")

    if category_id in categories_df["category_id"].values:
        raise ValueError("Category ID already exists.")

    new_category = pd.DataFrame([
        {
            "category_id": category_id,
            "category_name": category_name
        }
    ])

    categories_df = pd.concat(
        [categories_df, new_category],
        ignore_index=True
    )

    return {
        "message": "Category created successfully.",
        "category_id": category_id
    }


def get_category(category_id):
    category_id = int(category_id)

    result = categories_df[
        categories_df["category_id"] == category_id
    ]

    if result.empty:
        raise ValueError("Category not found.")

    return result.iloc[0].to_dict()


def get_all_categories():
    return categories_df.to_dict(orient="records")


def category_exists(category_id):
    category_id = int(category_id)

    return category_id in categories_df["category_id"].values


def update_category(category_id, category_name):
    global categories_df

    category_id = int(category_id)
    category_name = str(category_name).strip()

    if not category_name:
        raise ValueError("Category name cannot be empty.")

    mask = categories_df["category_id"] == category_id

    if not mask.any():
        raise ValueError("Category not found.")

    categories_df.loc[mask, "category_name"] = category_name

    return {
        "message": "Category updated successfully."
    }


def delete_category(category_id):
    global categories_df

    category_id = int(category_id)

    mask = categories_df["category_id"] == category_id

    if not mask.any():
        raise ValueError("Category not found.")

    categories_df = categories_df[
        ~mask
    ].reset_index(drop=True)

    return {
        "message": "Category deleted successfully."
    }