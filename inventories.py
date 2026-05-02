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
    ["Number of Calls", "Energy Demand (TJ)", "GHG Emissions (t CO2e)", 
     "NZF Costs in 2030 (US$)", "NZF Costs in 2040 (US$)", "NZF Costs in 2050 (US$)"]
)
indicator_cols = ["n_vys", "ene_tj", "co2e_t", "s24_30", "s24_40", "s24_50"]
if indicator == None:
    indicator = "Number of Calls"


### INVENTORIES BY VESSEL TYPE ###
st.header("{0} by Vessel Type".format(
    indicator))

# Read-in International Arrivals Inventory by Vessel Type Associated with the Country
int_arr_by_type_to_plot_cols = ["Int. Arr. by Type"] + indicator_cols
int_arr_by_type_to_plot = pd.read_csv(\
    input_dir + "inventories_v0.2/{0}/int_arr_by_type.csv".format(
        st.session_state.iso_code.replace(' ','%20')
    ), usecols=int_arr_by_type_to_plot_cols
)

int_arr_by_type_to_plot["inv_type"] = "Int. Arrivals"
int_arr_by_type_to_plot_col_renames = {
    "Int. Arr. by Type": "Vessel Type", "n_vys":"Number of Calls", 
    "ene_tj":"Energy Demand (TJ)", "co2e_t":"GHG Emissions (t CO2e)",
    "s24_30":"NZF Costs in 2030 (US$)", "s24_40":"NZF Costs in 2040 (US$)", "s24_50":"NZF Costs in 2050 (US$)"
}
int_arr_by_type_to_plot = int_arr_by_type_to_plot.rename(
    columns=int_arr_by_type_to_plot_col_renames
)


# Read-in International Departures Inventory by Vessel Type Associated with the Country
int_dep_by_type_to_plot_cols = ["Int. Dep. by Type"] + indicator_cols
int_dep_by_type_to_plot = pd.read_csv(
    input_dir + "inventories_v0.2/{0}/int_dep_by_type.csv".format(
        st.session_state.iso_code.replace(' ','%20')
    ), usecols=int_dep_by_type_to_plot_cols
)

int_dep_by_type_to_plot["inv_type"] = "Int. Departures"
int_dep_by_type_to_plot_col_renames = {
    "Int. Dep. by Type": "Vessel Type", "n_vys":"Number of Calls", 
    "ene_tj":"Energy Demand (TJ)", "co2e_t":"GHG Emissions (t CO2e)",
    "s24_30":"NZF Costs in 2030 (US$)", "s24_40":"NZF Costs in 2040 (US$)", "s24_50":"NZF Costs in 2050 (US$)"
}
int_dep_by_type_to_plot = int_dep_by_type_to_plot.rename(
    columns=int_dep_by_type_to_plot_col_renames
)


# Combine Int. Arrivals and Int. Departures Inventories for Plotting
int_inv_by_type_to_plot = pd.concat([int_arr_by_type_to_plot, int_dep_by_type_to_plot], axis=0)

# Plot depending on the value of Segmented Control
if indicator == "Number of Calls":
    st.altair_chart(
        alt.Chart(int_arr_by_type_to_plot).mark_bar().encode(
            x=alt.X("Vessel Type", sort='-y'),
            y="Number of Calls", # alt.Y(y, sort='-x')
            color="Number of Calls")
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
int_arr_by_partner_to_plot_cols = ["Int. Arr. by Partner"] + indicator_cols
int_arr_by_partner_to_plot = pd.read_csv(\
    input_dir + "inventories_v0.2/{0}/int_arr_by_partner.csv".format(
        st.session_state.iso_code.replace(' ','%20')
    ), usecols=int_arr_by_partner_to_plot_cols
)

int_arr_by_partner_to_plot["inv_type"] = "Int. Arrivals"
int_arr_by_partner_to_plot_col_renames = {
    "Int. Arr. by Partner": "Partner Economy", "n_vys": "Number of Calls", 
    "ene_tj": "Energy Demand (TJ)", "co2e_t": "GHG Emissions (t CO2e)",
    "s24_30":"NZF Costs in 2030 (US$)", "s24_40":"NZF Costs in 2040 (US$)", "s24_50":"NZF Costs in 2050 (US$)"
}
int_arr_by_partner_to_plot = int_arr_by_partner_to_plot.rename(
    columns=int_arr_by_partner_to_plot_col_renames
)


# Read-in International Departures Inventory by Vessel Type Associated with the Country
int_dep_by_partner_to_plot_cols = ["Int. Dep. by Partner"] + indicator_cols
int_dep_by_partner_to_plot = pd.read_csv(
    input_dir + "inventories_v0.2/{0}/int_dep_by_partner.csv".format(
        st.session_state.iso_code.replace(' ','%20')
    ), usecols=int_dep_by_partner_to_plot_cols
)

int_dep_by_partner_to_plot["inv_type"] = "Int. Departures"
int_dep_by_partner_to_plot_col_renames = {
    "Int. Dep. by Partner": "Partner Economy", "n_vys":"Number of Calls", 
    "ene_tj":"Energy Demand (TJ)", "co2e_t":"GHG Emissions (t CO2e)",
    "s24_30":"NZF Costs in 2030 (US$)", "s24_40":"NZF Costs in 2040 (US$)", "s24_50":"NZF Costs in 2050 (US$)"
}
int_dep_by_partner_to_plot = int_dep_by_partner_to_plot.rename(
    columns=int_dep_by_partner_to_plot_col_renames
)


# Combine Int. Arrivals and Int. Departures Inventories for Plotting
int_inv_by_partner_to_plot = pd.concat([int_arr_by_partner_to_plot, int_dep_by_partner_to_plot], axis=0)

# Plot depending on the value of Segmented Control
if indicator == "Number of Calls":
    st.altair_chart(
        alt.Chart(
            int_arr_by_partner_to_plot).mark_bar().encode(
            x=alt.X("Partner Economy", sort='-y'),
            y="Number of Calls", # alt.Y(y, sort='-x')
            color="Number of Calls")
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
int_arr_by_port_to_plot_cols = ["Int. Arr. by Port"] + indicator_cols
int_arr_by_port_to_plot = pd.read_csv(
    input_dir + "inventories_v0.2/{0}/int_arr_by_port.csv".format(
        st.session_state.iso_code.replace(' ','%20')
    ), usecols=int_arr_by_port_to_plot_cols)
int_arr_by_port_to_plot["inv_type"] = "Int. Arrivals"
int_arr_by_port_to_plot_col_renames = {
    "Int. Arr. by Port":"Port", "n_vys":"Number of Calls", 
    "ene_tj":"Energy Demand (TJ)", "co2e_t":"GHG Emissions (t CO2e)",
    "s24_30":"NZF Costs in 2030 (US$)", "s24_40":"NZF Costs in 2040 (US$)", "s24_50":"NZF Costs in 2050 (US$)"
}
int_arr_by_port_to_plot = int_arr_by_port_to_plot.rename(
    columns=int_arr_by_port_to_plot_col_renames
)

# Read-in International Departures Inventory by Vessel Type Associated with the Country
int_dep_by_port_to_plot_cols = ["Int. Dep. by Port"] + indicator_cols
int_dep_by_port_to_plot = pd.read_csv(
    input_dir + "inventories_v0.2/{0}/int_dep_by_port.csv".format(
        st.session_state.iso_code.replace(' ','%20')
    ), usecols=int_dep_by_port_to_plot_cols)

int_dep_by_port_to_plot["inv_type"] = "Int. Departures"
int_dep_by_port_to_plot_col_renames = {
    "Int. Dep. by Port":"Port", "n_vys":"Number of Calls", 
    "ene_tj":"Energy Demand (TJ)", "co2e_t":"GHG Emissions (t CO2e)",
    "s24_30":"NZF Costs in 2030 (US$)", "s24_40":"NZF Costs in 2040 (US$)", "s24_50":"NZF Costs in 2050 (US$)"
}
int_dep_by_port_to_plot = int_dep_by_port_to_plot.rename(
    columns=int_dep_by_port_to_plot_col_renames
)

# Combine Int. Arrivals and Int. Departures Inventories for Plotting
int_inv_by_port_to_plot = pd.concat([int_arr_by_port_to_plot, int_dep_by_port_to_plot], axis=0)

# Plot depending on the value of Segmented Control
if indicator == "Number of Calls":
    st.altair_chart(
        alt.Chart(int_arr_by_port_to_plot).mark_bar().encode(
            x=alt.X("Port", sort='-y'),
            y="Number of Calls", # alt.Y(y, sort='-x')
            color="Number of Calls")
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
