from os.path import join, abspath, pardir, dirname
import pandas as pd
import openfoodfacts
from argparse import ArgumentParser
from sys import argv

def print_log(text: str) -> None: print(f"[log] {text}")
def print_error(text: str) -> None: print(f"[error] {text}")

def fetch_categories() -> list:
    return openfoodfacts.facets.get_categories()

def preprocess_categories(category: dict) -> dict:
    return {
        "name": category.get('name'),
        "products": category.get('products'),
    }

def main() -> None:
    # Default configuration
    parent_dir = abspath(join(dirname(abspath(__file__)), pardir))
    data_dir = join(parent_dir, 'data')
    output_file = join(data_dir, 'categories.csv')

    # Fetch categories data
    print_log(f"Fetching all categories from 'openfoodfacts.org'")
    categories = fetch_categories()
    print_log(f"Found {len(categories)} categories")

    # Process categories data
    print_log(f"Processing categories data")
    categories = [preprocess_categories(c) for c in categories]

    # Save data
    print_log(f"Saving data to {data_dir}")
    df = pd.DataFrame(categories)
    df.to_csv(output_file, index=False)
    print_log(f"Saving data to {output_file}")

if __name__ == "__main__":
    main()
