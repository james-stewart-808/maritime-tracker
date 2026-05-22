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
    "Impact tracking results derived from the linking of: i) seaborne merchandise trade data for \
    2018 sourced from the UNCTAD Trade-and-Transport (UNCTAD, 2025), ii) AIS data underpinning the 4th IMO GHG \
    Study (Faber et al, 2020) and iii) assumptions of Maritime Transport Costs (MTCs) resulting from the IMO Net-Zero \
    Framework (NZF) based on Cost Intensity values derived from Task 2 of the Comprehensive Impact Assessment process \
    (DNV, 2024).")



### NZF ECONOMIC IMPACTS ###
st.title("Economic Impacts of the IMO Net-Zero Framework")
st.write(
    """
    The step aims to ensure that every tonne of trade associated with the seaborne component of a country’s international \
    merchandise trade portfolio is allocated to at least one representative vessel voyage, thereby enabling vessel-based \
    GHG emission estimates to be allocated to the seaborne trade portfolio in a realistic manner.

    A range of alternative approaches have been developed that seek to match international trade records with corresponding \
    transport supply estimations. Broadly, approaches separate into those that just utilise vessel-side AIS data fields to \
    estimate cargo volumes (Arslanalp et al, 2021; Arslanalp et al, 2025), versus others that also consider volumes of trade \
    explicitly defined in IMTS or UN Comtrade (Wang et al, 2021; Schim van der Loeff, 2025). The primary task of this process \
    is to identify the AIS-derived transport supply that facilitates each bilateral seaborne trade flow, i.e. the transport \
    supply that facilitates internationally traded volumes at the resolution of individual commodity headings and \
    origin-destination country pairs. It is recommended to compare and improve the mapping of bilateral trades to transport \
    supply where improved information and assumptions are available, for example through the analysis of manifest-level trade \
    records.
    
    - Bullet 1
    - Bullet 2
    """
)


impact_res_c = [
    "iso_code", "iso_country", "wb_gdp_2018", 
    "XI_vol_kg", "XI_vol_kg_recon", 
    "XI_val_usd", "XI_val_usd_recon", 
    "XI_ene_tj_recon", "XI_co2_t_recon",
    "XI_s24_usd_23_recon_del", "XI_s24_usd_30_recon_del", "XI_s24_usd_40_recon_del", "XI_s24_usd_50_recon_del",
    "XI_s24_del_23_pct_gdp", "XI_s24_del_30_pct_gdp", "XI_s24_del_40_pct_gdp", "XI_s24_del_50_pct_gdp"
]
impact_res_r = {
    
    # Country Stats
    "iso_country": "Country",
    "wb_gdp_2018": "GDP (2018)",
    "XI_vol_kg": "Trade Portfolio Volume (kg)", 
    "XI_val_usd": "Trade Portfolio Value (US$)", 

    # Trade Reconstruction Stats
    "XI_vol_kg_recon": "Reconstructed Trade Volume (kg)", 
    "XI_val_usd_recon": "Reconstructed Trade Value (US$)", 
    "XI_ene_tj_recon": "Reconstructed Trade Energy Demand (TJ)", 
    "XI_co2_t_recon": "Reconstructed Trade CO2 Emissions (t)", 

    # NZF Compliance Costs (S24 delta from BAU)
    "XI_s24_usd_23_recon_del": "NZF Incremental Cost in 2023 (US$)", 
    "XI_s24_usd_30_recon_del": "NZF Incremental Cost in 2030 (US$)", 
    "XI_s24_usd_40_recon_del": "NZF Incremental Cost in 2040 (US$)", 
    "XI_s24_usd_50_recon_del": "NZF Incremental Cost in 2050 (US$)",
    "XI_s24_del_23_pct_gdp": "NZF Incremental Cost in 2023 (%GDP)", 
    "XI_s24_del_30_pct_gdp": "NZF Incremental Cost in 2030 (%GDP)", 
    "XI_s24_del_40_pct_gdp": "NZF Incremental Cost in 2040 (%GDP)", 
    "XI_s24_del_50_pct_gdp": "NZF Incremental Cost in 2050 (%GDP)"
}

impact_res = pd.read_csv(
    input_dir + "res_coun_f.csv",
    dtype={"iso_code":"str"}
).rename(columns=impact_res_r)

impact_res_so = impact_res.sort_values(by="NZF Incremental Cost in 2050 (%GDP)", ascending=False).reset_index(drop=True)
impact_res_cou = impact_res_so[(impact_res_so.iso_code == st.session_state.iso_code)]
impact_res_cou_rank = impact_res_cou.index.values[0]+1


st.subheader(
    "Economic Impacts on {0}".format(
        st.session_state.iso_country),
    divider = 'grey'
)

st.markdown("##### Global IMO NZF Compliance Costs to 2050")
combined_df = pd.DataFrame(data={
    "Year":["2023", "2030", "2040", "2050"],
    "IMO NZF (US$bn)":[
        round(impact_res_so["NZF Incremental Cost in 2023 (US$)"].sum() / 1e9, 1),
        round(impact_res_so["NZF Incremental Cost in 2030 (US$)"].sum() / 1e9, 1),
        round(impact_res_so["NZF Incremental Cost in 2040 (US$)"].sum() / 1e9, 1),
        round(impact_res_so["NZF Incremental Cost in 2050 (US$)"].sum() / 1e9, 1)
    ]})

st.altair_chart(
    alt.Chart(combined_df).mark_line().encode(
        x=alt.X("Year"),
        y=alt.Y(
            alt.repeat("layer"),
            aggregate="mean",
            title="Mean of Compliance Costs (US$bn)"),
        color=alt.datum(alt.repeat("layer")),
        ).repeat(layer=[
            "IMO NZF (US$bn)"
    ]),
    width="stretch"
)
download_as_csv(
    combined_df, 
    "IMO NZF Impacts", 
    "Global IMO NZF Compliance Costs to 2050.csv"
)
st.divider()


st.markdown("##### Country-specific Results")
st.caption("Top 25 Countries in terms of Impacts Generated by the IMO NZF in 2050 - by % share of GDP")
st.altair_chart(
    alt.Chart(impact_res_so.sort_values(by="NZF Incremental Cost in 2050 (%GDP)", ascending=False).iloc[:25]).mark_bar().encode(
        x=alt.X("Country", sort='-y'),
        y=alt.Y("NZF Incremental Cost in 2050 (%GDP)"),
        color="NZF Incremental Cost in 2050 (%GDP)"))

impact_res_cou_cols=[
    "Country", 
    "Reconstructed Trade Volume (kg)", "Reconstructed Trade Value (US$)", 
    "Reconstructed Trade Energy Demand (TJ)", "Reconstructed Trade CO2 Emissions (t)", 
    "NZF Incremental Cost in 2023 (US$)", "NZF Incremental Cost in 2023 (%GDP)", 
    "NZF Incremental Cost in 2030 (US$)", "NZF Incremental Cost in 2030 (%GDP)", 
    "NZF Incremental Cost in 2040 (US$)", "NZF Incremental Cost in 2040 (%GDP)", 
    "NZF Incremental Cost in 2050 (US$)", "NZF Incremental Cost in 2050 (%GDP)"
]
impact_res_cou_display = impact_res_cou[impact_res_cou_cols].round(2).T

impact_res_cou_display = impact_res_cou_display.apply(
    lambda col: col.map(lambda x: f"{x:,.2f}" if isinstance(x, (int, float)) else x)
)
st.write(impact_res_cou_display)
download_as_csv(
    impact_res_cou[impact_res_cou_cols].T, 
    "IMO NZF Impacts for {0} ({1})".format(
        st.session_state.iso_country, st.session_state.iso_code),
    "IMO NZF Impacts for {0} ({1}).csv".format(
        st.session_state.iso_country, st.session_state.iso_code)
)
st.divider()


st.markdown("##### References")

st.write(
"""
DNV. (2024). Report of the Comprehensive impact assessment of the basket of \
    candidate GHG reduction mid-term measures – full report on Task 2 (Impacts \
    on the fleet). MEPC 82-INF.8-Add.1.
    
Faber et al. (2020). Fourth IMO Greenhouse Gas Study. London.
    
UNCTAD. (2025). Trade-and-Transport Dataset - Documentation.
"""
)
