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


### NZF ECONOMIC IMPACTS ###
st.title("Economic Impacts of the IMO Net-Zero Framework")
st.write(
    """
    A primary aim of the Maritime Tracker is to explore potential economic impacts arising from the IMO NZF. We have derived \
    estimates of what the economic impacts on the NZF will be for each voyage presented in the 'Voyage Inventories' page. By \
    conducting a matching process to link each individual bilateral trade flow of the country's Seaborne Trade Portfolio to \ 
    appropriate voyages in nation's Voyage Inventory, we can estimate what typical NZF cost impacts are for each trade flow, \
    then reconstruct the nation's entire Seaborne Trade Portfolio to derive total economic impacts on that economy. The total \
    aggregate NZF costs associated with all identified voyage is presented below.
    """
)

st.caption("Global IMO NZF Compliance Costs to 2050")
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


st.write(
    """
    Specifically, this step aims to ensure that every tonne of trade associated with the seaborne component of a country’s international \
    seaborne trade portfolio is allocated to at least one representative vessel voyage, thereby enabling vessel-based \
    GHG emission estimates to be allocated to the seaborne trade portfolio in a realistic manner. A range of alternative \
    approaches have been developed that seek to match international trade records with corresponding transport supply \
    estimations. Broadly, approaches separate into those that just utilise vessel-side AIS data fields to \
    estimate cargo volumes (Arslanalp et al, 2021; Arslanalp et al, 2025), versus others that also consider volumes of trade \
    explicitly defined in IMTS or UN Comtrade (Wang et al, 2021; Schim van der Loeff, 2025). 
    
    For the purposes of this method, each bilateral trade record constituting the seaborne component of a country’s international \
    trade portfolio, we would now like to identify the relevant facilitating transport supply in terms of voyages and their \
    associated GHG emissions. To achieve this, we will iterate through the seaborne trade portfolio in terms of the volume and \
    value of individual trade records per origin country, destination country and commodity code (HS 2-digit) heading. For each \
    bilateral trade record, we will filter the voyages dataset using two criteria to identify relevant transport supply, discussed \
    in further detail below. The total NZF Compliance Costs are shown in the Figure below.
    """
)

st.markdown("##### Mapping Feasible Vessel Types to Commodity Headings")
st.write(
    """
    In order to understand the range of vessel types capable of facilitating alternative commodity flows, we take forward a dataset \
    of consignment-level Bills of Lading data from the Global Shipping Watch project, and use it to understand which vessel types \
    are most prevalent in facilitating the transportation of certain commodity headings (Schim van der Loeff et al, 2018). Consisting \
    of 13.2 million individual consignment records, the Global Shipping Watch dataset represents 1.4 billion tonnes and US$10.1tn \
    worth of goods associated with the export trade portfolios of the US, Brazil, Indonesia, Chile, Peru and Ghana - as well as US \
    imports - throughout 2019. First, the consignment-level trade records are merged with static vessel specifications data. The \
    resulting dataset is then grouped by commodity heading and vessel types identified as facilitating greater than 25% of each \
    commodity type by value are taken forward as those facilitating the transport of each commodity type.
    """
)
st.markdown("##### Identification of Feasible Routes")
st.write(
    """
    Another important consideration relates to the feasibility of alternative routes that facilitate a bilateral commodity trade. For \
    example, land-locked countries may utilise ports located in neighbouring countries to access international shipping service, whilst \
    a significant share of the trade portfolio associated with SIDS is likely to undergo transshipment at one point in the supply-chain \
    at least. It is therefore useful to consider the extent to which additional countries are involved in the supply-chain underpinning \
    a bilateral trade, as well as the likelihood of transshipment practises taking place. 

    For the purposes of this analysis, a matching of each economy to a set of countries whose ports are likely facilitate their trade \
    has been developed based on geographic proximity. It is assumed that a trade flow is facilitated by the direct voyages of vessels of \
    an appropriate type (as derived above), originating from - and destined for - ports identified in the facilitating origin or destination \
    sets of countries.
    """
)

st.markdown("##### Assigning Trade Volume to ‘Shipping Supply’")
st.write(
    """
    The next step will be to distribute the weight and value of each bilateral trade record across the shipping supply identified. In order \
    to achieve this, it is assumed that the weight, value and GHG emissions associated with each bilateral trade flow is distributed across \
    all identified voyages in proportion to the carrying capacity of each vessel. Utilisation factors differentiated by vessel class and \
    observed in the 4th IMO GHG Study are also applied to evaluate the assumed volume of cargo onboard each vessel. A new table can then be \
    established that indexes each voyage-trade pair to the fractional weight, value and GHG emissions of the cargo and voyage activity \
    associated with it. By reaggregating in terms of each bilateral trade flow record, the full international trade portfolio associated \
    with a country can be reconstructed in terms of the GHG emissions associated with its facilitating AIS-derived voyages.
    """
)

st.markdown("##### Conversion to Impacts on States")
st.write(
    """
    With the matching of NZF economic impacts and bilateral trade flows now complete, the next step will be to translate these bilateral \
    impacts onto economic impacts at the state level. Given that NZF costs are now mapped to bilateral trade flows in the international \
    seaborne trade portfolio, we are able to aggregate results across a number useful fields, the most important of which is by exporter or \
    importer commodity. For the purposes of this modelling approach, the economic impact for each country associated with the introduction of \
    the NZF is assumed to split equally between the country’s exporter-side and importer-side trade portfolio. By making comparison of each \
    result against the national GDP, the overall economic impact on each state is evaluated.
    """
)

st.caption("Top 25 Countries in terms of Impacts Generated by the IMO NZF in 2050 - by % share of GDP")
st.altair_chart(
    alt.Chart(impact_res_so.sort_values(by="NZF Incremental Cost in 2050 (%GDP)", ascending=False).iloc[:25]).mark_bar().encode(
        x=alt.X("Country", sort='-y'),
        y=alt.Y("NZF Incremental Cost in 2050 (%GDP)"),
        color="NZF Incremental Cost in 2050 (%GDP)"))


st.subheader(
    "Economic Impacts on {0}".format(
        st.session_state.iso_country),
    divider = 'grey'
)

st.markdown("##### Country-specific Results")
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
Arslanalp et al. (2021). Tracking Trade from Space: An Application to Pacific \
    Island Countries. IMF Working Paper No. 2021/225. Available at: \
    https://www.imf.org/en/Publications/WP/Issues/2021/08/20/\
    Tracking-Trade-from-Space-An-Application-to-Pacific-Island-Countries-464345

Arslanalp et al. (2025). Nowcasting Global Trade from Space. IMF Working Paper 25/93.

DNV. (2024). Report of the Comprehensive impact assessment of the basket of \
    candidate GHG reduction mid-term measures – full report on Task 2 (Impacts \
    on the fleet). MEPC 82-INF.8-Add.1.
    
Faber et al. (2020). Fourth IMO Greenhouse Gas Study. London.

Schim van der Loeff. (2025). Filling the Maritime Data Gap – A Big Data Approach \
    to Aligning Route-based Maritime Emissions, Transport Costs and Trade. Doctoral \
    thesis (Ph.D), University College London (UCL). Available at: \
    https://discovery.ucl.ac.uk/id/eprint/10208589/.

UNCTAD. (2025). Trade-and-Transport Dataset - Documentation.

Wang et al. (2021). Trade-linked shipping CO2 emissions. Nature Climate Change 11(11), \
    945–951. URL: https://www.nature.com/articles/s41558-021-01176-6.


"""
)
