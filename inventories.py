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

N_ene_co2 = st.segmented_control(
    "Would you like to visualise the Number of Port Calls, Energy Demand or Carbon Dioxide?",
    ["Number of Calls", "Energy Demand", "CO2 Emissions"]
)
if N_ene_co2 == None:
    N_ene_co2 = "Number of Calls"

### INVENTORIES BY VESSEL TYPE ###
st.header("{0} by Vessel Type".format(
    N_ene_co2))


# Read-in International Arrivals Inventory by Vessel Type Associated with the Country
int_arr_by_type_to_plot_cols = ["Int. Arr. by Type", "n_vys", "ene_tj", "co2e_t"]
int_arr_by_type_to_plot = pd.read_csv(\
    input_dir + "inventories_v0.2/{0}/int_arr_by_type.csv".format(
        st.session_state.iso_code.replace(' ','%20')
    ), usecols=int_arr_by_type_to_plot_cols
)

int_arr_by_type_to_plot["inv_type"] = "Int. Arrivals"
int_arr_by_type_to_plot_col_renames = {
    "Int. Arr. by Type": "Vessel Type", "n_vys":"Number of Calls", 
    "ene_tj":"Energy Demand (TJ)", "co2e_t":"GHG Emissions (t CO2e)"
}
int_arr_by_type_to_plot = int_arr_by_type_to_plot.rename(
    columns=int_arr_by_type_to_plot_col_renames
)


# Read-in International Departures Inventory by Vessel Type Associated with the Country
int_dep_by_type_to_plot_cols = ["Int. Dep. by Type", "n_vys", "ene_tj", "co2e_t"]
int_dep_by_type_to_plot = pd.read_csv(
    input_dir + "inventories_v0.2/{0}/int_dep_by_type.csv".format(
        st.session_state.iso_code.replace(' ','%20')
    ), usecols=int_dep_by_type_to_plot_cols
)

int_dep_by_type_to_plot["inv_type"] = "Int. Departures"
int_dep_by_type_to_plot_col_renames = {
    "Int. Dep. by Type": "Vessel Type", "n_vys":"Number of Calls", 
    "ene_tj":"Energy Demand (TJ)", "co2e_t":"GHG Emissions (t CO2e)"
}
int_dep_by_type_to_plot = int_dep_by_type_to_plot.rename(
    columns=int_dep_by_type_to_plot_col_renames
)


# Combine Int. Arrivals and Int. Departures Inventories for Plotting
int_inv_by_type_to_plot = pd.concat([int_arr_by_type_to_plot, int_dep_by_type_to_plot], axis=0)

# Plot depending on the value of Segmented Control
if N_ene_co2 == "Number of Calls":
    st.altair_chart(
        alt.Chart(int_arr_by_type_to_plot).mark_bar().encode(
            x=alt.X("Vessel Type", sort='-y'),
            y="Number of Calls", # alt.Y(y, sort='-x')
            color="Number of Calls")
    )

elif N_ene_co2 == "Energy Demand":
    st.bar_chart(
        int_inv_by_type_to_plot, 
        x="Vessel Type", 
        y="Energy Demand (TJ)", 
        color="inv_type", 
        stack=False
    )
else:
    st.bar_chart(
        int_inv_by_type_to_plot, 
        x="Vessel Type", 
        y="GHG Emissions (t CO2e)", 
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


### INVENTORIES BY PORT ###
st.header("{0} by Port of Interest".format(N_ene_co2))

# Read-in International Arrivals Inventory by Vessel Type Associated with the Country
int_arr_by_port_to_plot_cols = ["Int. Arr. by Port", "n_vys", "ene_tj", "co2e_t"]
int_arr_by_port_to_plot = pd.read_csv(
    input_dir + "inventories_v0.2/{0}/int_arr_by_port.csv".format(
        st.session_state.iso_code.replace(' ','%20')
    ), usecols=int_arr_by_port_to_plot_cols)
int_arr_by_port_to_plot["inv_type"] = "Int. Arrivals"
int_arr_by_port_to_plot_col_renames = {
    "Int. Arr. by Port":"Port", "n_vys":"Number of Calls", 
    "ene_tj":"Energy Demand (TJ)", "co2e_t":"Carbon Dioxide (t)"
}
int_arr_by_port_to_plot = int_arr_by_port_to_plot.rename(
    columns=int_arr_by_port_to_plot_col_renames
)

# Read-in International Departures Inventory by Vessel Type Associated with the Country
int_dep_by_port_to_plot_cols = ["Int. Dep. by Port", "n_vys", "ene_tj", "co2e_t"]
int_dep_by_port_to_plot = pd.read_csv(
    input_dir + "inventories_v0.2/{0}/int_dep_by_port.csv".format(
        st.session_state.iso_code.replace(' ','%20')
    ), usecols=int_dep_by_port_to_plot_cols)

int_dep_by_port_to_plot["inv_type"] = "Int. Departures"
int_dep_by_port_to_plot_col_renames = {
    "Int. Dep. by Port":"Port", "n_vys":"Number of Calls", 
    "ene_tj":"Energy Demand (TJ)", "co2e_t":"GHG Emissions (t CO2e)"
}
int_dep_by_port_to_plot = int_dep_by_port_to_plot.rename(
    columns=int_dep_by_port_to_plot_col_renames
)

# Combine Int. Arrivals and Int. Departures Inventories for Plotting
int_inv_by_port_to_plot = pd.concat([int_arr_by_port_to_plot, int_dep_by_port_to_plot], axis=0)

# Plot depending on the value of Segmented Control
if N_ene_co2 == "Number of Calls":
    st.altair_chart(
        alt.Chart(int_arr_by_port_to_plot).mark_bar().encode(
            x=alt.X("Port", sort='-y'),
            y="Number of Calls", # alt.Y(y, sort='-x')
            color="Number of Calls")
    )
elif N_ene_co2 == "Energy Demand":
    st.bar_chart(
        int_inv_by_port_to_plot, 
        x="Port", 
        y="Energy Demand (TJ)", 
        color="inv_type", 
        stack=False
    )
else:
    st.bar_chart(
        int_inv_by_port_to_plot, 
        x="Port", 
        y="GHG Emissions (t CO2e)", 
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
