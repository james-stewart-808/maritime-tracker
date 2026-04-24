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


##### MERCHANDISE TRADE PORTFOLIOS ######
# Incorporate Comtrade Data Availability Tracker

st.title("Merchandise Trade Portfolio for {0}".format(st.session_state.iso_country))
st.sidebar.markdown("International Merchandise Trade Portfolios Sourced from UNCTAD's Trade-and-Transport Database.")

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
    # Top Trade Flows
    if usd_t == "Value, $":
        st.header("Top Export Trade Flows by Value")
        tr_profile = "X_tr_usd"
        tr = pd.read_csv(
            input_dir + "portfolios_v0.2/{0}/{1}.csv".format(\
                st.session_state.iso_code, tr_profile), index_col=0)
        merch_trade_vis(tr.iloc[:25], "clean_desc", "USD")
    else:
        st.header("Top Export Trade Flows by Weight")
        tr_profile = "X_tr_t"
        tr = pd.read_csv(
            input_dir + "portfolios_v0.2/{0}/{1}.csv".format(\
                st.session_state.iso_code, tr_profile), index_col=0)
        merch_trade_vis(tr.iloc[:25], "clean_desc", "tonne")

    download_as_csv(
        tr, 
        "Top Export Trade Flows - {0} ({1})".format(st.session_state.iso_country, st.session_state.iso_code),
        "Top Export Trade Flows - {0} ({1}).csv".format(st.session_state.iso_country, st.session_state.iso_code)
    )

    # Top HS2 Commodity Flows
    if usd_t == "Value, $":
        st.header("Top Export HS2 Commodity Flows by Value")
        co_profile = "X_co_usd"
        co = pd.read_csv(
            input_dir + "portfolios_v0.2/{0}/{1}.csv".format(\
                st.session_state.iso_code, co_profile), index_col=0)
        merch_trade_vis(co.iloc[:25], "Description", "USD")
        st.write(co.iloc[:5][["HS2", "Description", "USD"]])
    else:
        st.header("Top Export HS2 Commodity Flows by Weight")
        co_profile = "X_co_t"
        co = pd.read_csv(
            input_dir + "portfolios_v0.2/{0}/{1}.csv".format(\
                st.session_state.iso_code, co_profile), index_col=0)
        merch_trade_vis(co.iloc[:25], "Description", "tonne")
        st.write(co.iloc[:5][["HS2", "Description", "tonne"]])

    download_as_csv(
        co, 
        "Top Export HS2 Commodity Flows - {0} ({1})".format(st.session_state.iso_country, st.session_state.iso_code),
        "Top Export HS2 Commodity Flows - {0} ({1}).csv".format(st.session_state.iso_country, st.session_state.iso_code)
    )

    # Top Partner Economies
    if usd_t == "Value, $":
        st.header("Top Export Partner Countries by Value")
        pa_profile = "X_pa_usd"
        pa = pd.read_csv(
            input_dir + "portfolios_v0.2/{0}/{1}.csv".format(\
                st.session_state.iso_code, pa_profile), index_col=0)
        merch_trade_vis(pa.iloc[:25], "imp_name", "USD")
    else:
        st.header("Top Export Partner Countries by Weight")
        pa_profile = "X_pa_t"
        pa = pd.read_csv(
            input_dir + "portfolios_v0.2/{0}/{1}.csv".format(\
                st.session_state.iso_code, pa_profile), index_col=0)
        merch_trade_vis(pa.iloc[:25], "imp_name", "tonne")
        #st.write(pa.iloc[:5][["imp_name", "tonne"]])

    download_as_csv(
        pa, 
        "Top Export Partner Countries - {0} ({1})".format(st.session_state.iso_country, st.session_state.iso_code),
        "Top Export Partner Countries - {0} ({1}).csv".format(st.session_state.iso_country, st.session_state.iso_code)
    )


### IMPORTS ###
else:
    # Top Trade Flows
    if usd_t == "Value, $":
        st.header("Top Import Trade Flows by Value")
        tr_profile = "I_tr_usd"
        tr = pd.read_csv(
            input_dir + "portfolios_v0.2/{0}/{1}.csv".format(\
                st.session_state.iso_code, tr_profile), index_col=0)
        merch_trade_vis(tr.iloc[:25], "clean_desc", "USD")
    else:
        st.header("Top Import Trade Flows by Weight")
        tr_profile = "I_tr_t"
        tr = pd.read_csv(
            input_dir + "portfolios_v0.2/{0}/{1}.csv".format(\
                st.session_state.iso_code, tr_profile), index_col=0)
        merch_trade_vis(tr.iloc[:25], "clean_desc", "tonne")

    download_as_csv(
        tr, 
        "Top Import Trade Flows - {0} ({1})".format(st.session_state.iso_country, st.session_state.iso_code),
        "Top Import Trade Flows - {0} ({1}).csv".format(st.session_state.iso_country, st.session_state.iso_code)
    )

    # Top HS2 Commodity Flows
    if usd_t == "Value, $":
        st.header("Top Import HS2 Commodity Flows by Value")
        co_profile = "I_co_usd"
        co = pd.read_csv(
            input_dir + "portfolios_v0.2/{0}/{1}.csv".format(\
                st.session_state.iso_code, co_profile), index_col=0)
        merch_trade_vis(co.iloc[:25], "Description", "USD")
    else:
        st.header("Top Import HS2 Commodity Flows by Weight")
        co_profile = "I_co_t"
        co = pd.read_csv(
            input_dir + "portfolios_v0.2/{0}/{1}.csv".format(\
                st.session_state.iso_code, co_profile), index_col=0)
        merch_trade_vis(co.iloc[:25], "Description", "tonne")

    download_as_csv(
        co, 
        "Top Import HS2 Commodity Flows - {0} ({1})".format(st.session_state.iso_country, st.session_state.iso_code),
        "Top Import HS2 Commodity Flows - {0} ({1}).csv".format(st.session_state.iso_country, st.session_state.iso_code)
    )

    # Top Partner Economies
    if usd_t == "Value, $":
        st.header("Top Import Partner Countries by Value")
        pa_profile = "I_pa_usd"
        pa = pd.read_csv(
            input_dir + "portfolios_v0.2/{0}/{1}.csv".format(\
                st.session_state.iso_code, pa_profile), index_col=0)
        merch_trade_vis(pa.iloc[:25], "exp_name", "USD")
    else:
        st.header("Top Import Partner Countries by Weight")
        pa_profile = "I_pa_t"
        pa = pd.read_csv(
            input_dir + "portfolios_v0.2/{0}/{1}.csv".format(\
                st.session_state.iso_code, pa_profile), index_col=0)
        merch_trade_vis(pa.iloc[:25], "exp_name", "tonne")

    download_as_csv(
        pa, 
        "Top Import Partner Countries - {0} ({1}).csv".format(st.session_state.iso_country, st.session_state.iso_code),
        "Top Import Partner Countries - {0} ({1}).csv".format(st.session_state.iso_country, st.session_state.iso_code)
    )


st.header("A note on Quality Assurance")
st.markdown(" - It's important to note that UNCTAD's Trade-and-Transport Database is fundamentally based on Comtrade data.")
st.markdown(" - The quality of data hosted on Comtrade is highly variable depending on the country and region.")
st.markdown(" - Presented below is the Comtrade contribution record for the selected country of interest over the decade from 2014-23.")
st.markdown(" - Please bear this information in-mind when exploring the trade data - merchandise trade statistics will be more reliable for countries that have provided their data often over recent years.")

by_country_contrib_record_v1 = pd.read_csv(
    input_dir + "by_country_contrib_record_v1.csv")
#st.write(by_country_contrib_record_v1)

def com_cont_aggregator(df, aggregator):
    df_group_cols = {"iso_code":"count", "2014":"sum", "2015":"sum", "2016":"sum", "2017":"sum", "2018":"sum", "2019":"sum", "2020":"sum", "2021":"sum", "2022":"sum", "2023":"sum"}
    df_grouped = df.groupby(aggregator).agg(df_group_cols).reset_index()
    df_grouped["Contributions"] = df_grouped["2014"] + df_grouped["2015"] + df_grouped["2016"] + df_grouped["2017"] + df_grouped["2018"] + df_grouped["2019"] + df_grouped["2020"] + df_grouped["2021"] + df_grouped["2022"] + df_grouped["2023"]
    df_grouped["Agg Totals"] = df_grouped["iso_code"] * 10
    df_grouped["Contribution (pct)"] = np.round(100 * df_grouped["Contributions"] / df_grouped["Agg Totals"], 1)
    return df_grouped#[[aggregator, "Contribution (pct)"]]


st.subheader("Overall Contribution Record of All States")
contributed = sum([by_country_contrib_record_v1[x].value_counts().values[0] for x in ["2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023"]])
total = by_country_contrib_record_v1.shape[0] * 10
contributed_frac = np.round(100 * contributed / (by_country_contrib_record_v1.shape[0] * 10), 1)
st.write("All countries for which data is available: {0} contributions over the last 10 years out of a possible {1}, representing an overall record of {2}%".format(contributed, total, contributed_frac))

comtrade_rec_cou = by_country_contrib_record_v1[(by_country_contrib_record_v1.iso_code == float(st.session_state.iso_code))]
if comtrade_rec_cou.shape[0] == 0:
    st.markdown("The Comtrade contribution record for {0} isn't available.".format(st.session_state.iso_country))
else:
    c1, c2, c3, c4, c5 = st.columns(5)
    c6, c7, c8, c9, c10 = st.columns(5)
    c1.metric("2014", comtrade_rec_cou["2014"].values[0])
    c2.metric("2015", comtrade_rec_cou["2015"].values[0])
    c3.metric("2016", comtrade_rec_cou["2016"].values[0])
    c4.metric("2017", comtrade_rec_cou["2017"].values[0])
    c5.metric("2018", comtrade_rec_cou["2018"].values[0])
    c6.metric("2019", comtrade_rec_cou["2019"].values[0])
    c7.metric("2020", comtrade_rec_cou["2020"].values[0])
    c8.metric("2021", comtrade_rec_cou["2021"].values[0])
    c9.metric("2022", comtrade_rec_cou["2022"].values[0])
    c10.metric("2023", comtrade_rec_cou["2023"].values[0])

    st.write("The contribution record of {0} over the last 10 years is shown above, representing an average contribution rate of {1}%. Further information on Comtrade Contribution Rates is provided below.".format(st.session_state.iso_country, int(100 * comtrade_rec_cou.iloc[:, -10:].sum().sum() / 10)))


    st.subheader("Contribution of Statistics by Region")
    #st.write(com_cont_aggregator(by_country_contrib_record_v1, "region_wb"))
    merch_trade_vis(com_cont_aggregator(by_country_contrib_record_v1, "region_wb"), "region_wb", "Contribution (pct)")

    st.subheader("Contribution Statistics by Geographic Status")
    #st.write(com_cont_aggregator(by_country_contrib_record_v1, "status"))
    merch_trade_vis(com_cont_aggregator(by_country_contrib_record_v1, "status"), "status", "Contribution (pct)")

    st.subheader("Contribution Statistics by Income Level")
    #st.write(com_cont_aggregator(by_country_contrib_record_v1, "income"))
    merch_trade_vis(com_cont_aggregator(by_country_contrib_record_v1, "income"), "income", "Contribution (pct)")

    st.subheader("Contribution Statistics by Region and Geographic Status")
    region_status_res = com_cont_aggregator(by_country_contrib_record_v1, ["region_wb", "status"])
    #st.write(region_status_res)
    region_status_res["clean_desc"] = region_status_res.region_wb + " " + region_status_res.status
    merch_trade_vis(region_status_res, "clean_desc", "Contribution (pct)")



##
