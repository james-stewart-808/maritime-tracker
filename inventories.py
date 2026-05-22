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
    "International Voyage-based Maritime Activity Inventories Disaggregated by Port and Vessel Type, Sourced from the \
    4th IMO GHG Study (Faber et al, 2020)."
)


##### INTERNATIONAL VOYAGE-BASED ACTIVITY INVENTORIES ######

st.title("Voyage Inventories")

st.write(
    """
    One of the key intentions of the dashboard is to summarise shipping activity associated with alternative countries. \
    For the purposes of the dashboard, we will use identification and analysis of voyages as the primary mechanism through \
    which to explore trends in maritime activity associated with each country. Specifically, we will consider collections, \
    or ‘inventories’, of voyage records associated with internationally arriving voyages and international departing voyages.\
    Voyage data is taken from the 4th IMO GHG Study (Faber et al, 2020). The study utilises AIS to understand the activity \
    profiles of individual vessels, then introduces vessel specification datasets that enable the energy demands, fuel \
    consumption and GHG emissions of vessel activity to be estimated. A full summary of the methodology used to estimate \
    GHG emissions from AIS data is presented in **Annex 1** of the Method Statement document. Initially comprised of 58,539 \
    voyages, the dataset is first filtered for vessel types associated with the international merchant fleet facilitating \
    the movement of goods by sea and resulting in a dataset representing 618.2 million tonnes of CO2 emissions.
    """
)
st.write(
    """
    The constitution of shipping activity occurring within the ports of a country are highly significant in terms of \
    characterisation of that country’s economic activity, and its analysis can provide useful insights into aspects of \
    economic behaviour such as relative geographic remoteness, distances to market and the scale of potential decarbonisation \
    and GHG mitigation. In order to explore such use cases, we can deploy a range of analytical metrics with which to summarise \
    the maritime activity associated with each country, where each is discussed in greater detail in the Table below with \
    respect to a set of voyages identified as belonging to each inventory.
    """
)
st.table(
    {
        "Number of Voyages": "The total number of voyages in the inventory.",
        "Fleet Size": "The total number of unique IMO numbers in the set of voyages.",
        "Transport Supply": "The sum of total transport work conducted by vessels across all voyages within the set. Transport \
            Work is provided in two separate forms, one calculation that represents the product of Gross Tonnage and distance \
            and another that represents the product of Deadweight Tonnage and distance.",
        "Average Build Year": "The average build year of vessels conducting voyages in the set. A range of averages are \
            provided, including the average observed across all voyages, the average across all vessels, as well as the average \
            build year when weighted by Gross Tonnage and Deadweight Tonnage.",
        "Average Voyage Distance": "The average distance associated with voyages in each inventory set. A number of alternative \
            metrics are provided, including the median distance travelled, the mean of median voyages completed by each vessel, \
            the average voyage distance weighted by Gross Tonnage and that weighted by Deadweight Tonnage.",
        "Average Voyage Time": "The average time taken for each voyage in the inventory set is also provided in terms of the \
            overall median observed in the set of voyages, the mean of median voyage times completed by each vessel, as well as \
            the average voyage time observed once weighted by Gross Tonnage or Deadweight Tonnage.",
        "Average Time in Port": "The average time in port observed for voyages in the inventory set is also provided on the \
            platform. The average time in port is provided in terms of the overall mean value observed in the set of voyages, as \
            well as the mean to median times in port associated with each vessel. The average time in port observed once weighted \
            by Gross Tonnage or Deadweight Tonnage is also provided.",
        "Energy Demand": "The sum of all energy demanded across the set of voyages. The calculation methodology for evaluation of \
            Energy Demand associated with each voyage is presented in **Annex 1** of the Method Statement.",
        "GHG Emissions": "The sum of all CO2-equivalent emissions generated across the set of voyages. The calculation methodology \
            for evaluation of GHG emissions associated with each voyage is presented in **Annex 1** of the Method Statement."
    },
    border="horizontal",
    width="stretch",
)
st.write(
    """
    In addition to the metrics described in Table , the economic impacts of the Net-Zero Framework are evaluated in associated with \
    each voyage. To do so, we will introduce results of the techno-economic fleet modelling undertaken by DNV as part of Task 2 of \
    the Comprehensive Impact Assessment of the Basket of Potential Mid-term Measures (DNV, 2024). Specifically, we will take forward \
    projections of changes in vessel cost intensity for 2030, 2040 and 2050. The modelling results we will use will be those derived \
    under Scenario 24, corresponding with certain policy parameters. Cost Intensity changes associated with Scenario 24 of DNV’s \
    modelling under Task 2 of the CIA are utilised in the modelling as these are observed to most closely align with the NZF’s \
    architecture. 
    """
)
st.write(
    """
    The output of DNV’s work for Task 2 of the CIA is given in terms ‘Cost Intensity’. Cost Intensity refers to an estimated change \
    in costs per unit of ‘transport work’, i.e. t-nm, referring to one tonne transported across one nautical mile. Given that the \
    dataset underpinning the 4th IMO GHG Study dataset includes vessel specification fields such as vessel deadweight tonnage, as \
    well as the distance covered as part of each voyage, we are able to work out the total amount of ‘Transport Work’ associated with \
    each voyage. We may then combine this dataset with the outputs of DNV’s modelling under Scenario 24 to estimate indicative \
    voyage-level cost changes in 2030, 2040 and 2050 arising from implementation of the Net-Zero Framework. The final dataset provides \
    indicative values of what fleet-level cost impacts are likely to be in future, assuming no major change in fleet-wide vessel \
    activity.
    """
)


st.subheader(
    "International Voyage-based Activity Inventories for {0}".format(
        st.session_state.iso_country),
    divider = 'grey'
)
indicator = st.segmented_control(
    "Which indicator would you like to visualise?",
    ["Number of Calls", #"Average Build Year", 
     "Average Voyage Distance (nm)", 
     "Average Voyage Time (hours)", "Average Time in Port (hours)", 
     "Energy Demand (TJ)", "GHG Emissions (t CO2e)", 
     "NZF Costs in 2030 (US$)", "NZF Costs in 2040 (US$)", "NZF Costs in 2050 (US$)",
     "NZF Costs per Voyage in 2030 (US$)", "NZF Costs per Voyage in 2040 (US$)", "NZF Costs per Voyage in 2050 (US$)"]
)
indicator_c = ["n_vys", "aby_flt", "avd_flt", "avt_flt", "apt_flt", "ene_tj", "co2e_t", "s24_30", "s24_40", "s24_50", "s24_30_voy", "s24_40_voy", "s24_50_voy"]
indicator_r = {
    "n_vys":"Number of Calls", 
    "aby_flt":"Average Build Year", "avd_flt":"Average Voyage Distance (nm)", 
    "avt_flt":"Average Voyage Time (hours)", "apt_flt":"Average Time in Port (hours)", 
    "ene_tj":"Energy Demand (TJ)", "co2e_t":"GHG Emissions (t CO2e)",
    "s24_30":"NZF Costs in 2030 (US$)", "s24_40":"NZF Costs in 2040 (US$)", "s24_50":"NZF Costs in 2050 (US$)",
    "s24_30_voy":"NZF Costs per Voyage in 2030 (US$)", "s24_40_voy":"NZF Costs per Voyage in 2040 (US$)", "s24_50_voy":"NZF Costs per Voyage in 2050 (US$)"
}

if indicator == None:
    indicator = "Number of Calls"

st.divider()


### INVENTORIES BY VESSEL TYPE ###
st.markdown("##### {0} by Vessel Type".format(indicator))
#st.subheader("{0} by Vessel Type".format(indicator), divider='grey')

# Read-in International Arrivals Inventory by Vessel Type Associated with the Country
int_arr_by_type = pd.read_csv(\
    input_dir + "inventories_v0.2/{0}/int_arr_by_type.csv".format(
        st.session_state.iso_code
    ), usecols = ["Int. Arr. by Type"] + indicator_c
).rename(columns={"Int. Arr. by Type": "Vessel Type"} | indicator_r)
int_arr_by_type["inv_type"] = "Int. Arrivals"


# Read-in International Departures Inventory by Vessel Type Associated with the Country
int_dep_by_type = pd.read_csv(
    input_dir + "inventories_v0.2/{0}/int_dep_by_type.csv".format(
        st.session_state.iso_code
    ), usecols = ["Int. Dep. by Type"] + indicator_c
).rename(columns={"Int. Dep. by Type": "Vessel Type"} | indicator_r)
int_dep_by_type["inv_type"] = "Int. Departures"


# Combine Int. Arrivals and Int. Departures Inventories for Plotting
int_inv_by_type_to_plot = pd.concat([int_arr_by_type, int_dep_by_type], axis=0)

# Plot depending on the value of Segmented Control
if indicator in ["Number of Calls"]:
    st.altair_chart(
        alt.Chart(int_arr_by_type).mark_bar().encode(
            x=alt.X("Vessel Type", sort='-y'),
            y=indicator,
            color=indicator)
    )
else:
    st.bar_chart(
        int_inv_by_type_to_plot, 
        x="Vessel Type", 
        y=indicator, 
        color="inv_type", 
        stack=False
    )

# Provide option to download as CSV
download_as_csv(
    int_inv_by_type_to_plot, 
    "International Arrivals Inventory by Vessel Type - {0} ({1})".format(
        st.session_state.iso_country, st.session_state.iso_code),
    "International Arrivals Inventory by Vessel Type - {0} ({1}).csv".format(
        st.session_state.iso_country, st.session_state.iso_code)
)
st.divider()


### INVENTORIES BY PARTNER ECONOMY ###
st.markdown("##### {0} by Partner Economy".format(indicator))
#st.subheader("{0} by Partner Economy".format(indicator), divider='grey')

# Read-in International Arrivals Inventory by Vessel Type Associated with the Country
int_arr_by_partner = pd.read_csv(\
    input_dir + "inventories_v0.2/{0}/int_arr_by_partner.csv".format(
        st.session_state.iso_code
    ), usecols = ["Int. Arr. by Partner"] + indicator_c
).rename(columns={"Int. Arr. by Partner": "Partner Economy"} | indicator_r)
int_arr_by_partner["inv_type"] = "Int. Arrivals"


# Read-in International Departures Inventory by Vessel Type Associated with the Country
int_dep_by_partner = pd.read_csv(
    input_dir + "inventories_v0.2/{0}/int_dep_by_partner.csv".format(
        st.session_state.iso_code
    ), usecols = ["Int. Dep. by Partner"] + indicator_c
).rename(columns={"Int. Dep. by Partner": "Partner Economy"} | indicator_r)
int_dep_by_partner["inv_type"] = "Int. Departures"


# Combine Int. Arrivals and Int. Departures Inventories for Plotting
int_inv_by_partner_to_plot = pd.concat([int_arr_by_partner, int_dep_by_partner], axis=0)

# Plot depending on the value of Segmented Control
if indicator in ["Number of Calls"]:
    st.altair_chart(
        alt.Chart(
            int_arr_by_partner).mark_bar().encode(
            x=alt.X("Partner Economy", sort='-y'),
            y=indicator,
            color=indicator)
    )

else:
    st.bar_chart(
        int_inv_by_partner_to_plot, 
        x="Partner Economy", 
        y=indicator, 
        color="inv_type", 
        stack=False
    )

# Provide option to download as CSV
download_as_csv(
    int_inv_by_partner_to_plot, 
    "International Arrivals Inventory by Partner Economy - {0} ({1})".format(
        st.session_state.iso_country, st.session_state.iso_code),
    "International Arrivals Inventory by Partner Economy - {0} ({1}).csv".format(
        st.session_state.iso_country, st.session_state.iso_code)
)
st.divider()


### INVENTORIES BY PORT ###
st.markdown("##### {0} by Port".format(indicator))
#st.subheader("{0} by Port".format(indicator), divider='grey')

# Read-in International Arrivals Inventory by Vessel Type Associated with the Country
int_arr_by_port = pd.read_csv(
    input_dir + "inventories_v0.2/{0}/int_arr_by_port.csv".format(
        st.session_state.iso_code
    ), usecols = ["Int. Arr. by Port"] + indicator_c
).rename(columns={"Int. Arr. by Port": "Port"} | indicator_r)
int_arr_by_port["inv_type"] = "Int. Arrivals"


# Read-in International Departures Inventory by Vessel Type Associated with the Country
int_dep_by_port = pd.read_csv(
    input_dir + "inventories_v0.2/{0}/int_dep_by_port.csv".format(
        st.session_state.iso_code
    ), usecols = ["Int. Dep. by Port"] + indicator_c
).rename(columns={"Int. Dep. by Port": "Port"} | indicator_r)
int_dep_by_port["inv_type"] = "Int. Departures"


# Combine Int. Arrivals and Int. Departures Inventories for Plotting
int_inv_by_port_to_plot = pd.concat([int_arr_by_port, int_dep_by_port], axis=0)

# Plot depending on the value of Segmented Control
if indicator in ["Number of Calls"]:
    st.altair_chart(
        alt.Chart(int_arr_by_port).mark_bar().encode(
            x=alt.X("Port", sort='-y'),
            y=indicator,
            color=indicator)
    )
else:
    st.bar_chart(
        int_inv_by_port_to_plot, 
        x="Port", 
        y=indicator, 
        color="inv_type", 
        stack=False
    )

# Provide option to download as CSV
download_as_csv(
    int_inv_by_port_to_plot, 
    "International Arrivals Inventory by Port - {0} ({1})".format(
        st.session_state.iso_country, st.session_state.iso_code),
    "International Arrivals Inventory by Port - {0} ({1}).csv".format(
        st.session_state.iso_country, st.session_state.iso_code)
)
st.divider()


st.markdown("##### References")

st.write(
"""
DNV. (2024a). Report of the Comprehensive impact assessment of the basket of \
    candidate GHG reduction mid-term measures – full report on Task 2 (Impacts \
    on the fleet). MEPC 82-INF.8-Add.1.
    
Faber et al. (2020). Fourth IMO Greenhouse Gas Study. London.
"""
)
