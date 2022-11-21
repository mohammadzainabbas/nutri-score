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
    data_path = join(getcwd(), "data")


if __name__ == "__main__":
    main()