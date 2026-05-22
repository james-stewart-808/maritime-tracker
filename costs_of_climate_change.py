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
    "Costs of Climate Change data sourced from (Dean et al, 2021)."
)


##### COSTS OF CLIMATE CHANGE ######
st.set_page_config(layout='wide')
st.title('National Macroeconomic Effects of Climate Scenarios')

st.divider()

st.write(
    """
    Using data from Kahn et al. (2021) and Mohaddes and Raissi (2024) we are able to show country-specific annual GDP per-capita losses from global warming \
    using the most recent climate scenarios of the Intergovernmental Panel on Climate Change (IPCC). We have chosen this study for its thorough scope, covering 174 \
    countries and numerous SSP and RCP scenario combinations that range from optimistic to pessimistic as follows:
    
    • SSP1-2.6: A scenario consistent with Paris Agreement pledges projecting a sustainable future where global \
                warming is limited to below 2°C and between 1.5-1.8°C above the pre industrial average by 2100.  
    • SSP2-4.5: A 'middle of the road' scenario that most closely aligns with 1960-2014 trends where a 'business as usual' approach leads to around 2.7°C of warming.  
    • SSP3-7.0: A more pessimistic scenario reflecting policy reversals, low international cooperation and high material intensive consumption that leads to 3.6°C of warming.  
    • SSP5-8.5: A high emissions scenario where with intensive fossil fuel expansion and minimal climate mitigation. This is deemed unrealistic now but included to show a worst case scenario. 
             
    Furthermore, previous literature has projected the impact of increasing temperatures on GDP by using a counterfactual scenario where there \
    is 'no further warming'. The problem with this is that there are no realistic pathways to a scenario in which baseline temperatures would remain constant \
    leading to overstated loss predictions. Therefore, a more realistic counterfactual is proposed where temeprature in each country rises according to its trend \ 
    from 1960-2014. To calculate GDP losses in simple terms, a 30-year moving average temperature is used to represent the speed at which historical norms change, i.e how quickly \ 
    countries adapt to rising temperatures. This moving average is subtracted from the projected temperature for a given year to produce a gap. The same process is \ 
    carried out for the counterfactual world, where temperatures rise only at their modest historical pace, producing its own gap. \
    The counterfactual gap is then subtracted from the scenario gap, and it is this resulting temperature disparity, representing the extra warming that economies have not \ 
    yet adapted to, above and beyond what would have occurred anyway, that drives the estimated GDP losses. 
    Below, you can find data for your selected country, compare countries, and view the global picture through to 2100.
    """
)  


st.markdown("##### References")

st.write(
"""
Dean et al. (2021). Costs of Climate Change per Country.
"""
)
