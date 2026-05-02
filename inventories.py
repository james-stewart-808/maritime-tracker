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


##### INTERNATIONAL VOYAGE-BASED ACTIVITY INVENTORIES ######
# Re-write subset output scripts in terms country codes (e.g. '007') and include 'Disaggregation by Partner Countries'.

st.title(
    "International Voyage-based Activity Inventories for {0}".format(
        st.session_state.iso_country)
)
st.sidebar.markdown(
    "International Voyage-based Maritime Activity Inventories Disaggregated by Port and Vessel Type, Sourced from the \
    4th IMO GHG Study (Faber et al, 2020)."
)

indicator = st.segmented_control(
    "Which indicator would you like to visualise?",
    ["Number of Calls", 
     #"Ave. Build Year", 
     "Ave. Voyage Distance (nm)", 
     "Ave. Voyage Time (hours)", 
     "Ave. Time in Port (hours)", 
     "Energy Demand (TJ)", "GHG Emissions (t CO2e)", 
     "NZF Costs in 2030 (US$)", "NZF Costs in 2040 (US$)", "NZF Costs in 2050 (US$)"]
)
indicator_cols = ["n_vys", "aby_flt", "avd_flt", "avt_flt", "apt_flt", "ene_tj", "co2e_t", "s24_30", "s24_40", "s24_50"]
if indicator == None:
    indicator = "Number of Calls"


### INVENTORIES BY VESSEL TYPE ###
st.header("{0} by Vessel Type".format(indicator))

# Read-in International Arrivals Inventory by Vessel Type Associated with the Country
int_arr_by_type_r = {
    "Int. Arr. by Type": "Vessel Type", "n_vys":"Number of Calls", 
    "aby_flt":"Ave. Build Year", "avd_flt":"Ave. Voyage Distance (nm)", 
    "avt_flt":"Ave. Voyage Time (hours)", "apt_flt":"Ave. Time in Port (hours)", 
    "ene_tj":"Energy Demand (TJ)", "co2e_t":"GHG Emissions (t CO2e)",
    "s24_30":"NZF Costs in 2030 (US$)", "s24_40":"NZF Costs in 2040 (US$)", "s24_50":"NZF Costs in 2050 (US$)"
}
int_arr_by_type = pd.read_csv(\
    input_dir + "inventories_v0.2/{0}/int_arr_by_type.csv".format(
        st.session_state.iso_code.replace(' ','%20')
    ), usecols = ["Int. Arr. by Type"] + indicator_cols
).rename(
    columns=int_arr_by_type_r
)
int_arr_by_type["inv_type"] = "Int. Arrivals"


# Read-in International Departures Inventory by Vessel Type Associated with the Country
int_dep_by_type_r = {
    "Int. Dep. by Type": "Vessel Type", "n_vys":"Number of Calls", 
    "aby_flt":"Ave. Build Year", "avd_flt":"Ave. Voyage Distance (nm)", 
    "avt_flt":"Ave. Voyage Time (hours)", "apt_flt":"Ave. Time in Port (hours)", 
    "ene_tj":"Energy Demand (TJ)", "co2e_t":"GHG Emissions (t CO2e)",
    "s24_30":"NZF Costs in 2030 (US$)", "s24_40":"NZF Costs in 2040 (US$)", "s24_50":"NZF Costs in 2050 (US$)"
}
int_dep_by_type = pd.read_csv(
    input_dir + "inventories_v0.2/{0}/int_dep_by_type.csv".format(
        st.session_state.iso_code.replace(' ','%20')
    ), usecols = ["Int. Dep. by Type"] + indicator_cols
).rename(
    columns=int_dep_by_type_r
)
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




### INVENTORIES BY PARTNER ECONOMY ###
st.header("{0} by Partner Economy".format(
    indicator))

# Read-in International Arrivals Inventory by Vessel Type Associated with the Country
int_arr_by_partner_r = {
    "Int. Arr. by Partner": "Partner Economy", "n_vys": "Number of Calls",
    "aby_flt":"Ave. Build Year", "avd_flt":"Ave. Voyage Distance (nm)", 
    "avt_flt":"Ave. Voyage Time (hours)", "apt_flt":"Ave. Time in Port (hours)", 
    "ene_tj": "Energy Demand (TJ)", "co2e_t": "GHG Emissions (t CO2e)",
    "s24_30":"NZF Costs in 2030 (US$)", "s24_40":"NZF Costs in 2040 (US$)", "s24_50":"NZF Costs in 2050 (US$)"
}
int_arr_by_partner = pd.read_csv(\
    input_dir + "inventories_v0.2/{0}/int_arr_by_partner.csv".format(
        st.session_state.iso_code.replace(' ','%20')
    ), usecols = ["Int. Arr. by Partner"] + indicator_cols
).rename(
    columns=int_arr_by_partner_r
)
int_arr_by_partner["inv_type"] = "Int. Arrivals"


# Read-in International Departures Inventory by Vessel Type Associated with the Country
int_dep_by_partner_r = {
    "Int. Dep. by Partner": "Partner Economy", "n_vys":"Number of Calls", 
    "aby_flt":"Ave. Build Year", "avd_flt":"Ave. Voyage Distance (nm)", 
    "avt_flt":"Ave. Voyage Time (hours)", "apt_flt":"Ave. Time in Port (hours)", 
    "ene_tj":"Energy Demand (TJ)", "co2e_t":"GHG Emissions (t CO2e)",
    "s24_30":"NZF Costs in 2030 (US$)", "s24_40":"NZF Costs in 2040 (US$)", "s24_50":"NZF Costs in 2050 (US$)"
}
int_dep_by_partner = pd.read_csv(
    input_dir + "inventories_v0.2/{0}/int_dep_by_partner.csv".format(
        st.session_state.iso_code.replace(' ','%20')
    ), usecols = ["Int. Dep. by Partner"] + indicator_cols
).rename(
    columns=int_dep_by_partner_r
)
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




### INVENTORIES BY PORT ###
st.header("{0} by Port".format(indicator))

# Read-in International Arrivals Inventory by Vessel Type Associated with the Country
int_arr_by_port_r = {
    "Int. Arr. by Port":"Port", "n_vys":"Number of Calls", 
    "aby_flt":"Ave. Build Year", "avd_flt":"Ave. Voyage Distance (nm)", 
    "avt_flt":"Ave. Voyage Time (hours)", "apt_flt":"Ave. Time in Port (hours)", 
    "ene_tj":"Energy Demand (TJ)", "co2e_t":"GHG Emissions (t CO2e)",
    "s24_30":"NZF Costs in 2030 (US$)", "s24_40":"NZF Costs in 2040 (US$)", "s24_50":"NZF Costs in 2050 (US$)"
}
int_arr_by_port = pd.read_csv(
    input_dir + "inventories_v0.2/{0}/int_arr_by_port.csv".format(
        st.session_state.iso_code.replace(' ','%20')
    ), usecols = ["Int. Arr. by Port"] + indicator_cols
).rename(
    columns=int_arr_by_port_r
)
int_arr_by_port["inv_type"] = "Int. Arrivals"


# Read-in International Departures Inventory by Vessel Type Associated with the Country
int_dep_by_port_r = {
    "Int. Dep. by Port":"Port", "n_vys":"Number of Calls", 
    "aby_flt":"Ave. Build Year", "avd_flt":"Ave. Voyage Distance (nm)", 
    "avt_flt":"Ave. Voyage Time (hours)", "apt_flt":"Ave. Time in Port (hours)", 
    "ene_tj":"Energy Demand (TJ)", "co2e_t":"GHG Emissions (t CO2e)",
    "s24_30":"NZF Costs in 2030 (US$)", "s24_40":"NZF Costs in 2040 (US$)", "s24_50":"NZF Costs in 2050 (US$)"
}
int_dep_by_port = pd.read_csv(
    input_dir + "inventories_v0.2/{0}/int_dep_by_port.csv".format(
        st.session_state.iso_code.replace(' ','%20')
    ), usecols = ["Int. Dep. by Port"] + indicator_cols
).rename(
    columns=int_dep_by_port_r
)
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
