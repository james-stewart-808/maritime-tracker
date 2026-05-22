import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
import time
input_dir = "https://raw.githubusercontent.com/james-stewart-808/inventory-tracker/main/datasets/"

def download_as_csv(file, label, filename):
    return st.download_button(
            data=file.to_csv(index=False),
            label=label,
            file_name=filename)

st.sidebar.markdown(
    "Costs of Climate Change data sourced from (Dean et al, 2021)."
)


##### COSTS OF CLIMATE CHANGE ######
st.markdown("##### Costs of Climate Change for {0}".format(
    st.session_state.iso_country))

st.write(
    """
    Costs of Climate Change data.
    """
)
st.divider()


st.markdown("##### References")

st.write(
"""
Dean et al. (2021). Costs of Climate Change per Country.
"""
)
