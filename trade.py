import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
import time
input_dir = "https://raw.githubusercontent.com/james-stewart-808/inventory-tracker/main/datasets/"

def merch_trade_vis(dataset, x, y):
    return st.altair_chart(
        alt.Chart(dataset).mark_bar().encode(
            x=alt.X(x, sort='-y', title=None),
            y=y,
            color=y))

def download_as_csv(file, label, filename):
    return st.download_button(
            data=file.to_csv(index=False),
            label=label,
            file_name=filename)

st.sidebar.markdown(
    "International Merchandise Trade Portfolios Sourced from UNCTAD's Trade-and-Transport Database."
)


##### SEABORNE TRADE PORTFOLIOS ######
st.title("Seaborne Trade Portfolio")
st.write(
    """
    The figures made use of for the dashboard are taken from UNCTAD’s Trade-and-Transport database for the year 2018 (UNCTAD, 2025). \
    The dataset records international trade, in values and volumes, alongside the transport expenditure and transport work incurred \
    for its transport per bilateral trade pair, commodity and mode of transport between 2016 and 2021. The data contained represents \
    237 economies of origin and 170 economies of destination, broken down by commodity group at the level of headings of the Harmonized \
    System classification (4-digit level, 2017 revision) and differentiating between air, sea, rail and road (Halim et al, 2018; \
    Hoffmeister et al, 2022; UNSD, 2011). The database is utilised here for its sophisticated approach to isolating the seaborne component \
    of international trade flows, which is a key requisite for its association with maritime activity.
    """
)


st.subheader(
    "Seaborne Trade Portfolio for {0}".format(
        st.session_state.iso_country),
    divider = 'grey'
)

# Consider Imports or Exports?
I_X = st.segmented_control(
    "Would you like to visualise Exports or Imports?", ["Exports", "Imports"])
if I_X == None:
    I_X = "Exports"

usd_t = st.segmented_control(
    "Are you interested in trade value or volume?", ["Value, $", "Weight, t"])
if usd_t == None:
    usd_t = "Value, $"

### EXPORTS ###
if I_X == "Exports":

    st.divider()
    # Top Trade Flows
    if usd_t == "Value, $":
        st.markdown("##### Top Export Trade Flows by Value")
        tr_profile = "X_tr_usd"
        tr = pd.read_csv(
            input_dir + "portfolios_v0.2/{0}/{1}.csv".format(
                st.session_state.iso_code, tr_profile), index_col=0)
        merch_trade_vis(tr.iloc[:25], "clean_desc", "USD")
    else:
        st.markdown("##### Top Export Trade Flows by Weight")
        tr_profile = "X_tr_t"
        tr = pd.read_csv(
            input_dir + "portfolios_v0.2/{0}/{1}.csv".format(\
                st.session_state.iso_code, tr_profile), index_col=0)
        merch_trade_vis(tr.iloc[:25], "clean_desc", "tonne")

    download_as_csv(
        tr, 
        "Top Export Trade Flows - {0} ({1})".format(
            st.session_state.iso_country, st.session_state.iso_code),
        "Top Export Trade Flows - {0} ({1}).csv".format(
            st.session_state.iso_country, st.session_state.iso_code)
    )
    st.divider()
    
    # Top HS2 Commodity Flows
    if usd_t == "Value, $":
        st.markdown("##### Top Export HS2 Commodity Flows by Value")
        co_profile = "X_co_usd"
        co = pd.read_csv(
            input_dir + "portfolios_v0.2/{0}/{1}.csv".format(
                st.session_state.iso_code, co_profile), index_col=0)
        merch_trade_vis(co.iloc[:25], "Description", "USD")
    else:
        st.markdown("##### Top Export HS2 Commodity Flows by Weight")
        co_profile = "X_co_t"
        co = pd.read_csv(
            input_dir + "portfolios_v0.2/{0}/{1}.csv".format(\
                st.session_state.iso_code, co_profile), index_col=0)
        merch_trade_vis(co.iloc[:25], "Description", "tonne")

    download_as_csv(
        co, 
        "Top Export HS2 Commodity Flows - {0} ({1})".format(
            st.session_state.iso_country, st.session_state.iso_code),
        "Top Export HS2 Commodity Flows - {0} ({1}).csv".format(
            st.session_state.iso_country, st.session_state.iso_code)
    )
    st.divider()
    
    # Top Partner Economies
    if usd_t == "Value, $":
        st.markdown("##### Top Export Partner Countries by Value")
        pa_profile = "X_pa_usd"
        pa = pd.read_csv(
            input_dir + "portfolios_v0.2/{0}/{1}.csv".format(
                st.session_state.iso_code, pa_profile), index_col=0)
        merch_trade_vis(pa.iloc[:25], "imp_name", "USD")
    else:
        st.markdown("##### Top Export Partner Countries by Weight")
        pa_profile = "X_pa_t"
        pa = pd.read_csv(
            input_dir + "portfolios_v0.2/{0}/{1}.csv".format(
                st.session_state.iso_code, pa_profile), index_col=0)
        merch_trade_vis(pa.iloc[:25], "imp_name", "tonne")

    download_as_csv(
        pa, 
        "Top Export Partner Countries - {0} ({1})".format(
            st.session_state.iso_country, st.session_state.iso_code),
        "Top Export Partner Countries - {0} ({1}).csv".format(
            st.session_state.iso_country, st.session_state.iso_code)
    )
    st.divider()

### IMPORTS ###
else:
    # Top Trade Flows
    if usd_t == "Value, $":
        st.markdown("##### Top Import Trade Flows by Value")
        tr_profile = "I_tr_usd"
        tr = pd.read_csv(
            input_dir + "portfolios_v0.2/{0}/{1}.csv".format(
                st.session_state.iso_code, tr_profile), index_col=0)
        merch_trade_vis(tr.iloc[:25], "clean_desc", "USD")
    else:
        st.markdown("##### Top Import Trade Flows by Weight")
        tr_profile = "I_tr_t"
        tr = pd.read_csv(
            input_dir + "portfolios_v0.2/{0}/{1}.csv".format(
                st.session_state.iso_code, tr_profile), index_col=0)
        merch_trade_vis(tr.iloc[:25], "clean_desc", "tonne")

    download_as_csv(
        tr, 
        "Top Import Trade Flows - {0} ({1})".format(
            st.session_state.iso_country, st.session_state.iso_code),
        "Top Import Trade Flows - {0} ({1}).csv".format(
            st.session_state.iso_country, st.session_state.iso_code)
    )
    st.divider()
    
    # Top HS2 Commodity Flows
    if usd_t == "Value, $":
        st.markdown("##### Top Import HS2 Commodity Flows by Value")
        co_profile = "I_co_usd"
        co = pd.read_csv(
            input_dir + "portfolios_v0.2/{0}/{1}.csv".format(
                st.session_state.iso_code, co_profile), index_col=0)
        merch_trade_vis(co.iloc[:25], "Description", "USD")
    else:
        st.markdown("##### Top Import HS2 Commodity Flows by Weight")
        co_profile = "I_co_t"
        co = pd.read_csv(
            input_dir + "portfolios_v0.2/{0}/{1}.csv".format(
                st.session_state.iso_code, co_profile), index_col=0)
        merch_trade_vis(co.iloc[:25], "Description", "tonne")

    download_as_csv(
        co, 
        "Top Import HS2 Commodity Flows - {0} ({1})".format(
            st.session_state.iso_country, st.session_state.iso_code),
        "Top Import HS2 Commodity Flows - {0} ({1}).csv".format(
            st.session_state.iso_country, st.session_state.iso_code)
    )
    st.divider()
    
    # Top Partner Economies
    if usd_t == "Value, $":
        st.markdown("##### Top Import Partner Countries by Value")
        pa_profile = "I_pa_usd"
        pa = pd.read_csv(
            input_dir + "portfolios_v0.2/{0}/{1}.csv".format(
                st.session_state.iso_code, pa_profile), index_col=0)
        merch_trade_vis(pa.iloc[:25], "exp_name", "USD")
    else:
        st.markdown("##### Top Import Partner Countries by Weight")
        pa_profile = "I_pa_t"
        pa = pd.read_csv(
            input_dir + "portfolios_v0.2/{0}/{1}.csv".format(
                st.session_state.iso_code, pa_profile), index_col=0)
        merch_trade_vis(pa.iloc[:25], "exp_name", "tonne")

    download_as_csv(
        pa, 
        "Top Import Partner Countries - {0} ({1}).csv".format(
            st.session_state.iso_country, st.session_state.iso_code),
        "Top Import Partner Countries - {0} ({1}).csv".format(
            st.session_state.iso_country, st.session_state.iso_code)
    )
    st.divider()


st.markdown("##### References")

st.write(
"""
Hoffmeister and Dalheimer. (2024). A linear model to estimate modal split in \
    international freight transport, based on revealed preferences about cost \
    and time saving. J. Shipp. Trd. 9, 28. Available at: \
    https://doi.org/10.1186/s41072-024-00181-0.
    
UNCTAD. (2025). Trade-and-Transport Dataset - Documentation.
"""
)
