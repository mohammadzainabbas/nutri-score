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

def fetch_products(category: str, required_columns: list, total_data_points: int) -> list:
    products = list()
    i = 0
    for _product in openfoodfacts.products.get_all_by_category(category):
        all_columns = list(_product.keys())
        invalid = False
        for c in required_columns:
            if c not in all_columns: invalid = True
        if invalid: continue
        products.append(_product)
        if i >= total_data_points: break
        i += 1


def main() -> None:
    # Default configuration
    category_name = "Plant-based foods"
    total_data_points = 1000
    parent_dir = abspath(join(getcwd(), pardir))
    data_dir = join(parent_dir, 'data')
    
    column_mapping = column_mapping()


    # Fetch categories data
    print_log(f"Fetching all categories from OpenFoodFacts")
    categories = openfoodfacts.facets.get_categories()
    print_log(f"Found {len(categories)} categories")

    # Find category
    category = list(filter(lambda c: c['name'] == category_name, categories))[0]
    print_log(f"Found category {category['name']} with {category['products']} products")

    # Fetch products
    print_log(f"Fetching {total_data_points} products from category {category_name}")
    data = fetch_products(category.get('id'), total_data_points)



if __name__ == "__main__":
    main()