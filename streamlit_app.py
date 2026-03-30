import streamlit as st
import pandas as pd

# Define the pages
main = st.Page("main.py", title="Home", icon="🏡")
inventories = st.Page("inventories.py", title="Voyage-based Inventories", icon="🚢")
trade = st.Page("trade.py", title="Merchandise Trade Portfolios", icon="📦")
impact_tracking = st.Page("impact_tracking.py", title="Impact Tracking Results", icon="💵")

# Set up navigation
pg = st.navigation([main, inventories])#, trade, impact_tracking]) #, example_page])

# Run the selected page
pg.run()
