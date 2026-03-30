import streamlit as st
st.header("Welcome to the Homepage of the International Shipping Dashboard 🏡")

country_iso_codes = pd.read_csv("/country_iso_codes.csv")#, usecols=country_iso_codes_cols, dtype=country_iso_codes_dtype).rename(columns=country_iso_codes_renames)
#country_iso_codes.loc[country_iso_codes.iso_country == "Namibia", "iso_2"] = "NA"
print(country_iso_codes.head(2))
