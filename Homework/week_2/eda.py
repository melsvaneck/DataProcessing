#!/usr/bin/env python
# Name:Mels van Eck
# Student number:12505757
"""
This script visualizes data obtained from a .csv file
it will show: “Country”, “Region”,
 “Pop. Density (per sq. mi.)”,
 “Infant mortality (per 1000 births)”
 and “GDP ($ per capita) dollars”.
"""

import csv
import pandas as pd
from pandas import DataFrame

INPUT_CSV = "input.csv"




if __name__ == "__main__":

    data = pd.read_csv(INPUT_CSV )

    data.set_index(("Country"), inplace=True)
    print(data.iloc[:,2:6].head(5))
