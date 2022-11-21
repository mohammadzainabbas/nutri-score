from os import getcwd
from os.path import join, abspath, pardir, relpath, exists
from dataclasses import dataclass, field
import pandas as pd
import numpy as np
import openfoodfacts
import requests

def print_log(text: str) -> None: print(f"[log] {text}")
def print_error(text: str) -> None: print(f"[error] {text}")

def main() -> None:
    # Default configuration
    category_name = "Plant-based foods"
    total_data_points = 1000
    parent_dir = abspath(join(getcwd(), pardir))
    data_dir = join(parent_dir, 'data')

    # Fetch categories data
    print_log(f"Fetching all categories from OpenFoodFacts")
    categories = openfoodfacts.facets.get_categories()
    print_log(f"Found {len(categories)} categories")

    # Find category
    category = list(filter(lambda c: c['name'] == category_name, categories))[0]
    print_log(f"Found category {category['name']} with {category['products']} products")

    # Fetch products
    print_log(f"Fetching {total_data_points} products from category {category_name}")
    




if __name__ == "__main__":
    main()