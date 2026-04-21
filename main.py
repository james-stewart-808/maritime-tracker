import pandas as pd
import requests
from io import StringIO
import streamlit as st
st.header("Welcome to the Homepage of the International Shipping Dashboard 🏡")

st.caption(
    "Explore global maritime shipping, merchandise trade portfolios, "
    "and economic impact tracking across countries."
)

st.divider()


# Load Country ISO data
country_iso_codes_c = ["name", "alpha-2", "alpha-3", "country-code"]
country_iso_codes_d = {"alpha-2":str, "alpha-3":str, "country-code":str}
country_iso_codes_r = {"name":"iso_country", "alpha-2":"iso_2", "alpha-3":"iso_3", "country-code":"iso_code"}

country_iso_codes = pd.read_csv(
  "https://raw.githubusercontent.com/james-stewart-808/inventory-tracker/main/datasets/country_iso_codes.csv",
  usecols=country_iso_codes_c, 
  dtype=country_iso_codes_d).rename(
  columns=country_iso_codes_r)

# Fix Namibia ISO issue
country_iso_codes.loc[country_iso_codes.iso_country == "Namibia", "iso_2"] = "NA"
country_iso_codes.loc[country_iso_codes.iso_country == "Congo, Democratic Republic of the", "iso_country"] = "Democratic Republic of the Congo"

# Country Selector
country_choice = st.selectbox(
    "For which country would you like to statistics related to international shipping, merchandise trade and MTM impact tracking?",
    country_iso_codes.iso_country.unique(),
    index=2)

# set as global variable
st.session_state.iso_country = country_choice
st.session_state.iso_2 = country_iso_codes[(country_iso_codes.iso_country == country_choice)].iso_2.values[0]
st.session_state.iso_3 = country_iso_codes[(country_iso_codes.iso_country == country_choice)].iso_3.values[0]
st.session_state.iso_code = country_iso_codes[(country_iso_codes.iso_country == country_choice)].iso_code.values[0]

# Homepage Description

st.divider()

st.write(
"""
Use the sidebar to explore the different components of the dashboard.

🚢 **Voyage-based Inventories** – Track shipping movements and inventories.

📦 **Merchandise Trade Portfolios** – Analyse import/export flows by commodity and partner.

💵 **Impact Tracking Results** – Monitor trade impacts and economic metrics.
"""
)
