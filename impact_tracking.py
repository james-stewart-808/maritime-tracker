import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
import time

def download_as_csv(file, label, filename):
    return st.download_button(
            data=file.to_csv(index=False),
            label=label,
            file_name=filename)

st.sidebar.markdown("Impact tracking results derived from the linking of: i) seaborne merchandise trade data for 2018 sourced from the UNCTAD Trade-and-Transport, ii) AIS data underpinning the 4th IMO GHG Study and iii) assumptions of Maritime Transport Costs (MTCs) resulting from the IMO Net-Zero Framework (NZF).")

impact_res_ex_c = [
    "source_iso_code", "source_country", "gdp_2018_wb", "vol_kg", "val_usd",
    "vol_kg_recon", "val_usd_recon", "ene_tj_recon", "co2_t_recon",
    "ets_23_usd_recon", "ets_30_usd_recon", "ets_23_pct_gdp", "ets_30_pct_gdp", 
    "bau_usd_23_recon", "bau_usd_30_recon", "bau_usd_40_recon", "bau_usd_50_recon",
    "bau_23_pct_gdp", "bau_30_pct_gdp", "bau_40_pct_gdp", "bau_50_pct_gdp", 
    "s24_usd_23_recon_del", "s24_usd_30_recon_del", "s24_usd_40_recon_del", "s24_usd_50_recon_del",
    "s24_del_23_pct_gdp", "s24_del_30_pct_gdp", "s24_del_40_pct_gdp", "s24_del_50_pct_gdp"
]
impact_res_ex_r = {
    
    # Country Stats
    "source_country":"Country",
    "gdp_2018_wb":"GDP (2018)",
    "vol_kg":"Trade Portfolio Volume (kg)", 
    "val_usd":"Trade Portfolio Value (US$)", 

    # Trade Reconstruction Stats
    "vol_kg_recon":"Reconstructed Trade Volume (kg)", 
    "val_usd_recon":"Reconstructed Trade Value (US$)", 
    "ene_tj_recon":"Reconstructed Trade Energy Demand (TJ)", 
    "co2_t_recon":"Reconstructed Trade CO2 Emissions (t)", 

    # ETS Compliance Costs
    "ets_23_usd_recon":"ETS Compliance Costs in 2023 (US$)", 
    "ets_30_usd_recon":"ETS Compliance Costs in 2030 (US$)", 
    "ets_23_pct_gdp":"ETS Compliance Costs in 2023 (%GDP)", 
    "ets_30_pct_gdp":"ETS Compliance Costs in 2030 (%GDP)",

    # NZF Compliance Costs (BAU Only)
    "bau_usd_23_recon":"BAU Costs in 2023 (US$)", 
    "bau_usd_30_recon":"BAU Costs in 2030 (US$)", 
    "bau_usd_40_recon":"BAU Costs in 2040 (US$)", 
    "bau_usd_50_recon":"BAU Costs in 2050 (US$)",
    "bau_23_pct_gdp":"BAU Costs in 2023 (%GDP)", 
    "bau_30_pct_gdp":"BAU Costs in 2030 (%GDP)", 
    "bau_40_pct_gdp":"BAU Costs in 2040 (%GDP)", 
    "bau_50_pct_gdp":"BAU Costs in 2050 (%GDP)", 

    # NZF Compliance Costs (S24 delta from BAU)
    "s24_usd_23_recon_del":"NZF Incremental Cost in 2023 (US$)", 
    "s24_usd_30_recon_del":"NZF Incremental Cost in 2030 (US$)", 
    "s24_usd_40_recon_del":"NZF Incremental Cost in 2040 (US$)", 
    "s24_usd_50_recon_del":"NZF Incremental Cost in 2050 (US$)",
    "s24_del_23_pct_gdp":"NZF Incremental Cost in 2023 (%GDP)", 
    "s24_del_30_pct_gdp":"NZF Incremental Cost in 2030 (%GDP)", 
    "s24_del_40_pct_gdp":"NZF Incremental Cost in 2040 (%GDP)", 
    "s24_del_50_pct_gdp":"NZF Incremental Cost in 2050 (%GDP)"
}

impact_res_ex = pd.read_csv(
    "https://raw.githubusercontent.com/james-stewart-808/inventory-tracker/main/datasets/impact_analysis_ex.csv",
    dtype={"source_iso_code":"str"}
).rename(columns=impact_res_ex_r)

impact_res_ex_so = impact_res_ex.sort_values(by="NZF Incremental Cost in 2050 (%GDP)", ascending=False).reset_index(drop=True)
impact_res_ex_cou = impact_res_ex_so[(impact_res_ex_so.source_iso_code == st.session_state.iso_code)]
impact_res_ex_cou_rank = impact_res_ex_cou.index.values[0]+1

st.title("Key Impact Tracking Results for {0}".format(st.session_state.iso_country))

st.write("\
Using the voyages dataset to model the compliance costs costs associated with the EU ETS and IMO NZF, we are now in a \
position to explore the relative impacts of these two policy measures on alternative states. You have the option to just \
focus on costs associated with the EU ETS, the IMO NZF, or a combination of them both.")


st.header("Global EU ETS vs IMO NZF Compliance Costs to 2050")
combined_df = pd.DataFrame(data={
    "Year":["2023", "2030", "2040", "2050"],
    "EU ETS (US$bn)":[
        round(impact_res_ex_so["ETS Compliance Costs in 2023 (US$)"].sum() / 1e9, 1),
        round(impact_res_ex_so["ETS Compliance Costs in 2030 (US$)"].sum() / 1e9, 1),
        None, 
        None
    ],
    "IMO NZF (US$bn)":[
        round(impact_res_ex_so["NZF Incremental Cost in 2023 (US$)"].sum() / 1e9, 1),
        round(impact_res_ex_so["NZF Incremental Cost in 2030 (US$)"].sum() / 1e9, 1),
        round(impact_res_ex_so["NZF Incremental Cost in 2040 (US$)"].sum() / 1e9, 1),
        round(impact_res_ex_so["NZF Incremental Cost in 2050 (US$)"].sum() / 1e9, 1)
    ]})

st.altair_chart(
    alt.Chart(combined_df).mark_line().encode(
        x=alt.X("Year"),
        y=alt.Y(
            alt.repeat("layer"),
            aggregate="mean",
            title="Mean of Compliance Costs (US$bn)"),
        color=alt.datum(alt.repeat("layer")),
        ).repeat(layer=["EU ETS (US$bn)", "IMO NZF (US$bn)"]),
    width="stretch"
)
download_as_csv(
    combined_df, 
    "EU ETS vs IMO NZF Impacts", 
    "Global EU ETS vs IMO NZF Compliance Costs to 2050.csv"
)

st.header("Policy-specific Results")
ETS_NZF = st.segmented_control(
    "Are you interested in econonic impacts from the EU ETS or the IMO NZF?",
    ["EU ETS", "IMO NZF"])
if ETS_NZF == None:
    ETS_NZF = "EU ETS"
    

if ETS_NZF == "EU ETS":
    st.caption("Top 25 Countries in terms of Impacts Generated by the EU ETS in 2030 - by % share of GDP")
    st.altair_chart(
        alt.Chart(impact_res_ex_so.sort_values(by="ETS Compliance Costs in 2030 (%GDP)", ascending=False).iloc[:25]).mark_bar().encode(
            x=alt.X("Country", sort='-y'),
            y=alt.Y("ETS Compliance Costs in 2030 (%GDP)"),
            color="ETS Compliance Costs in 2030 (%GDP)"))

    impact_res_ex_cou_cols=[
        "Country", 
        "Reconstructed Trade Volume (kg)", "Reconstructed Trade Value (US$)", "Reconstructed Trade Energy Demand (TJ)", "Reconstructed Trade CO2 Emissions (t)", 
        "ETS Compliance Costs in 2023 (US$)", "ETS Compliance Costs in 2023 (%GDP)", 
        "ETS Compliance Costs in 2030 (US$)", "ETS Compliance Costs in 2030 (%GDP)"
    ]
    st.write(impact_res_ex_cou[impact_res_ex_cou_cols].T)
    download_as_csv(
        impact_res_ex_cou[impact_res_ex_cou_cols].T, 
        "EU ETS Impacts for {0} ({1})".format(st.session_state.iso_country, st.session_state.iso_code),
        "EU ETS Impacts for {0} ({1}).csv".format(st.session_state.iso_country, st.session_state.iso_code)
    )

elif ETS_NZF == "IMO NZF":
    st.caption("Top 25 Countries in terms of Impacts Generated by the IMO NZF in 2030 - by % share of GDP")
    st.altair_chart(
        alt.Chart(impact_res_ex_so.sort_values(by="NZF Incremental Cost in 2023 (%GDP)", ascending=False).iloc[:25]).mark_bar().encode(
            x=alt.X("Country", sort='-y'),
            y=alt.Y("NZF Incremental Cost in 2030 (%GDP)"),
            color="NZF Incremental Cost in 2030 (%GDP)"))
    
    impact_res_ex_cou_cols=[
        "Country", 
        "Reconstructed Trade Volume (kg)", "Reconstructed Trade Value (US$)", "Reconstructed Trade Energy Demand (TJ)", "Reconstructed Trade CO2 Emissions (t)", 
        "NZF Incremental Cost in 2023 (US$)", "NZF Incremental Cost in 2023 (%GDP)", 
        "NZF Incremental Cost in 2030 (US$)", "NZF Incremental Cost in 2030 (%GDP)", 
        "NZF Incremental Cost in 2040 (US$)", "NZF Incremental Cost in 2040 (%GDP)", 
        "NZF Incremental Cost in 2050 (US$)", "NZF Incremental Cost in 2050 (%GDP)"
    ]
    st.write(impact_res_ex_cou[impact_res_ex_cou_cols].T)
    download_as_csv(
        impact_res_ex_cou[impact_res_ex_cou_cols].T, 
        "IMO NZF Impacts for {0} ({1})".format(st.session_state.iso_country, st.session_state.iso_code),
        "IMO NZF Impacts for {0} ({1}).csv".format(st.session_state.iso_country, st.session_state.iso_code)
    )

else:
    pass
