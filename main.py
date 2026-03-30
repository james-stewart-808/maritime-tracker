import pandas as pd
import requests
from io import StringIO
import streamlit as st
st.header("Welcome to the Homepage of the International Shipping Dashboard 🏡")

def load_original_data():
    url = 'https://raw.githubusercontent.com/james-stewart-808/inventory-tracker/main/datasets/dom_inv_by_vess_type.csv'
    response = requests.get(url)
    if response.status_code == 200:
        return pd.read_csv(StringIO(response.text), nrows=2)
    else:
        st.error("Failed to load data from GitHub.")
        return None
#country_iso_codes = load_original_data()

#country_iso_codes = pd.read_csv("https://raw.githubusercontent.com/james-stewart-808/inventory-tracker/main/datasets/dom_inv_by_vess_type.csv")

# Function to load the CSV file
@st.cache_data(scope="session")
def load_data(file):
    data = pd.read_csv(file)
    return data

country_iso_codes = load_data('https://raw.githubusercontent.com/james-stewart-808/inventory-tracker/main/datasets/dom_inv_by_vess_type.csv')


#country_iso_codes = pd.read_csv("/country_iso_codes.csv")#, usecols=country_iso_codes_cols, dtype=country_iso_codes_dtype).rename(columns=country_iso_codes_renames)
#country_iso_codes.loc[country_iso_codes.iso_country == "Namibia", "iso_2"] = "NA"

st.write(country_iso_codes)
#
