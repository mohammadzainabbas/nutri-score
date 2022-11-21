from os import getcwd
from os.path import join, abspath, pardir, relpath, exists
from dataclasses import dataclass, field
import pandas as pd
import numpy as np
import openfoodfacts
import requests

