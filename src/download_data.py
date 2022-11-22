from os.path import join, abspath, pardir, dirname
import pandas as pd
import openfoodfacts
from typing import List, Dict, Any
from argparse import ArgumentParser
from sys import argv

def print_log(text: str) -> None: print(f"[log] {text}")
def print_error(text: str) -> None: print(f"[error] {text}")

def columns_mapping() -> Dict[str, str]:
    return {
        "id": "id",
        "name": "product_name",
        "image_url": "image_url",
        "brand": "brands",
        "categories": "categories",
        "nutriscore_data": "nutriscore_data.all",
        "nutriments": "nutriments.all",
}

def get_mapping(data: Dict[str, Any], key: str, value: str) -> Dict[str, Any]:
    values = value.split(".")
    is_all = "all" in values
    _data = data
    for val in values:
        if is_all and val == "all": break
        _data = _data[val]
    return {key: _data} if not is_all else _data

def preprocess_products(product: Dict[str, Any], column_mapping: Dict[str, str]) -> Dict[str, Any]:
    _data = dict()
    for key in column_mapping.keys():
        _data.update(get_mapping(product, key, column_mapping[key]))
    return _data

def fetch_products(category: str, column_mapping: dict, required_columns: list, total_data_points: int) -> list:

    def check_required_columns(_product: dict, _required_columns: list) -> bool:
        return all([x in list(_product.keys()) for x in _required_columns])

    products = list()
    i = 0
    check_keys = ["is_beverage", "negative_points", "energy_points", "saturated_fat_points", "sugars_points", "sodium_points", "positive_points", "fiber_points", "proteins_points", "fruits_vegetables_nuts_colza_walnut_olive_oils_points"]
    for _product in openfoodfacts.products.get_all_by_category(category):
        # Check if we got correct data from the API
        invalid = not check_required_columns(_product, required_columns)
        if invalid: continue
        
        # Preprocess product data by mapping columns
        product = preprocess_products(_product, column_mapping)

        # Check if we got all the keys we need for sanity check
        invalid = not check_required_columns(product, check_keys)
        if invalid: continue
        
        # Check some sanity checks (for correctness)
        # 1. No drinks allowed
        if product.get("is_beverage") == float(1): invalid = True
        # 2. Invalid negative values
        if product.get("negative_points") != (product.get("energy_points") + product.get("saturated_fat_points") + product.get("sugars_points") + product.get("sodium_points")): invalid = True
        # 3. Invalid positive values
        if product.get("positive_points") != (product.get("fiber_points") + product.get("proteins_points") + product.get("fruits_vegetables_nuts_colza_walnut_olive_oils_points")): invalid = True
        
        if invalid: continue
        products.append(product)
        if (i + 1) >= total_data_points: break
        i += 1
    return products

def main(total_data_points: int = 100, category_name: str = "Plant-based foods") -> None:
    # Default configuration
    parent_dir = abspath(join(dirname(abspath(__file__)), pardir))
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

    basename = argv[0] if len(argv) else "download_data.py"
    parser = ArgumentParser(f"Script '{basename}' downloads data from 'openfoodfacts.org' and saves it")
    parser.add_argument("-t", "--total_datapoints", help="Total data-points to download and save, default: 100", type=int, default=100)
    parser.add_argument("-c","--category", help="Category for which you want the data, default: 'Plant-based foods'", type=str, default="Plant-based foods")
    # parser.add_argument("-p","--save_dir", help="Directory for data to be saved.", type=str, default="data")
    args = parser.parse_args()
    main(total_data_points=args.total_datapoints, category_name=args.category)
