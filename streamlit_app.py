import streamlit as st
import pandas as pd

# logo at the top of sidebar
st.markdown(
    """
    <style>
    [data-testid="stSidebarNav"]::before {
        content: "";
        display: block;
        margin: 0px auto 20px auto;
        height: 120px;
        width: 180px;
        background-image: url(https://raw.githubusercontent.com/james-stewart-808/maritime-tracker/main/UCL_Logo_S_1C_B_RGB_Energy-Inst.png);
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Define the pages
main = st.Page("main.py", title="Home", icon="🏡")
inventories = st.Page("inventories.py", title="Voyage-based Inventories", icon="🚢")
trade = st.Page("trade.py", title="Merchandise Trade Portfolios", icon="📦")
impact_tracking = st.Page("impact_tracking.py", title="Impact Tracking Results", icon="💵")

# Set up navigation
pg = st.navigation([main, inventories, trade, impact_tracking])

# Run the selected page
pg.run()
