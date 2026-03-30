import pandas as pd
import requests
from io import StringIO
import streamlit as st
st.header("Welcome to the Homepage of the International Shipping Dashboard 🏡")

country_iso_codes_cols = ["name", "alpha-2", "alpha-3", "country-code"]
country_iso_codes_dtype = {"alpha-2":str, "alpha-3":str, "country-code":str}
#country_iso_codes_renames = {"name":"iso_country", "alpha-2":"iso_2", "alpha-3":"iso_3", "country-code":"iso_code"}
#country_iso_codes = pd.read_csv(
#  "https://raw.githubusercontent.com/james-stewart-808/inventory-tracker/main/datasets/country_iso_codes.csv",
#  usecols=country_iso_codes_cols, 
#  dtype=country_iso_codes_dtype).rename(
#  columns=country_iso_codes_renames)
#country_iso_codes.loc[country_iso_codes.iso_country == "Namibia", "iso_2"] = "NA"

country_iso_codes = pd.read_csv(
  "https://raw.githubusercontent.com/james-stewart-808/inventory-tracker/main/datasets/country_iso_codes.csv",
  usecols=country_iso_codes_cols, 
  dtype=country_iso_codes_dtype,
  nrows=1
)

st.write(country_iso_codes.head())
#
