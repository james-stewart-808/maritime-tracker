import pandas as pd
import requests
from io import StringIO
import streamlit as st
st.header("Welcome to the Homepage of the International Shipping Dashboard 🏡")

#country_iso_codes = pd.read_csv("/country_iso_codes.csv")#, usecols=country_iso_codes_cols, dtype=country_iso_codes_dtype).rename(columns=country_iso_codes_renames)
#country_iso_codes.loc[country_iso_codes.iso_country == "Namibia", "iso_2"] = "NA"

def load_original_data():
    url = 'https://github.com/james-stewart-808/inventory-tracker/blob/7fbe5e3fbbee1753c4c47df552a594297d328df7/datasets/country_iso_codes.csv'
    response = requests.get(url)
    if response.status_code == 200:
        return pd.read_csv(StringIO(response.text), nrows=2)
    else:
        st.error("Failed to load data from GitHub.")
        return None
country_iso_codes = load_original_data()

print(country_iso_codes.head(2))
