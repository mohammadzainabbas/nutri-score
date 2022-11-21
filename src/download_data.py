from os import getcwd
from os.path import join, abspath, pardir, relpath, exists
from dataclasses import dataclass, field
import pandas as pd
import numpy as np
import openfoodfacts
import requests

def print_log(text: str) -> None: print(f"[log] {text}")
def print_error(text: str) -> None: print(f"[error] {text}")

def columns_mapping() -> dict:
    return {
        "id": "id",
        "name": "product_name",
        "image_url": "image_url",
        "brand": "brands",
        "categories": "categories",
        "nutriscore_data": "nutriscore_data.all",
        "nutriments": "nutriments.all",
}

def get_mapping(data, key, value):
    values = value.split(".")
    is_all = "all" in values
    _data = data
    for val in values:
        if is_all and val == "all": break
        _data = _data[val]
    return {key: _data} if not is_all else _data

def preprocess_products(product: dict, column_mapping: dict) -> dict:
    _data = dict()
    for key in column_mapping.keys():
        _data.update(get_mapping(product, key, column_mapping[key]))
    return _data

def fetch_products(category: str, column_mapping: dict, required_columns: list, total_data_points: int) -> list:
    products = list()
    i = 0
    for _product in openfoodfacts.products.get_all_by_category(category):
        all_columns = list(_product.keys())
        invalid = False
        for c in required_columns:
            if c not in all_columns: invalid = True
        if invalid: continue
        products.append(preprocess_products(_product, column_mapping))
        if i >= total_data_points: break
        i += 1

def main() -> None:
    # Default configuration
    category_name = "Plant-based foods"
    total_data_points = 5
    # parent_dir = abspath(join(getcwd(), pardir))
    parent_dir = abspath(join(getcwd(), pardir))
    data_dir = join(parent_dir, 'data')
    output_file = join(data_dir, 'products.csv')

    column_mapping = columns_mapping()
    required_columns = [x.split(".")[0] for x in list(column_mapping.values())]

    # Fetch categories data
    print_log(f"Fetching all categories from 'openfoodfacts.org'")
    categories = openfoodfacts.facets.get_categories()
    print_log(f"Found {len(categories)} categories")

    # Find category
    category = list(filter(lambda c: c['name'] == category_name, categories))[0]
    print_log(f"Found category {category['name']} with {category['products']} products")

    # Fetch products
    print_log(f"Fetching {total_data_points} products from category {category_name}")
    data = fetch_products(category.get('id'), column_mapping, required_columns, total_data_points)

    # Save data
    print_log(f"Saving data to {data_dir}")
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)
    print_log(f"Saving data to {output_file}")

if __name__ == "__main__":
    main()
