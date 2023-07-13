import matplotlib.animation as animation
import matplotlib.pyplot as plt
import streamlit as st
import plotly.colors as colors
from plotly.offline import iplot, init_notebook_mode
from matplotlib import cm
import plotly.io as pio
import plotly.express as px
import numpy as np
from json import load
import pandas as pd
import streamlit as st
import matplotlib.cm as cm
import pydeck as pdk
import Map as Mp
import calendar
import altair as alt

st.markdown("# Road Accident Analysis ")
st.sidebar.markdown("# Analysis Report ")
st.sidebar.info(
    "Road Accidents"
)

row1_col1, row1_col2 = st.columns(
    [0.8, 2]
)
row2_col1, row2_col2 = st.columns(
    [1.5, 1.5]
)
row3_col1, row3_col2, row3_col3 = st.columns(
    [1, 1, 1]
)
row4_col1, row4_col2, row4_col3 = st.columns(
    [1, 1, 1]
)
row5_col1, row5_col2 = st.columns(
    [1, 1]
)
row6_col1, row6_col2 = st.columns([4, 1])
# --------------------------------------------------------------------------------
with row1_col1:
    time_period2 = st.selectbox(
        "Select time period:", ["Monthly", "Yearly"])

# ---------------------------------------


def year_func2(yy):
    filtered2 = pd.DataFrame()
    for index, row in Mp.year_data.iterrows():
        if (row['year'] == yy):
            filtered2 = pd.concat([filtered2, row.to_frame().T])
    return filtered2


def month_func2(yy):
    filtered2 = pd.DataFrame()
    for index, row in Mp.month_data.iterrows():
        if (row['year'] == yy):
            filtered2 = pd.concat([filtered2, row.to_frame().T])
    return filtered2


# ----------------------------------all parts-----------------------------
if time_period2 == "Monthly":
    with row3_col1:
        year = st.slider("Select year:", 2020, 2023, 2020)
        filtered2_data = month_func2(year)
        if filtered2_data is not None and not filtered2_data.empty:
            Accidents = filtered2_data.groupby(
                'month')['Accidents'].sum().reset_index()

            Accidents['month'] = Accidents['month'].apply(
                lambda x: calendar.month_name[x])

            month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                           'July', 'August', 'September', 'October', 'November', 'December']

            Accidents['month'] = pd.Categorical(
                Accidents['month'], categories=month_order, ordered=True)
            Accidents = Accidents.sort_values('month')

            Accidents.reset_index(drop=True, inplace=True)

            chart = alt.Chart(Accidents).mark_line(point=True, stroke='red', color='red', opacity=1.0, strokeWidth=3).encode(
                x=alt.X('month', axis=alt.Axis(
                    labelAngle=0, labelColor='black', titleColor='black', titleOpacity=1.0), sort=month_order),
                y=alt.Y('Accidents', axis=alt.Axis(labelColor='black',
                        titleColor='black', titleOpacity=1.0)),
                tooltip=[
                    alt.Tooltip('month', title='Month'),
                    alt.Tooltip(
                        'Accidents', title='Accidents/Month', format='d')
                ]
            ).properties(
                width=850,
                height=700,
                title=" Accident Count / Month ",

            )
            st.altair_chart(chart)


if time_period2 == "Yearly":
    year_range = st.slider("Select year range:", 2020, 2023, (2020, 2021))
    start_year, end_year = year_range
    filtered2_data = []
    years = []
    Accidents = []
    for year in range(start_year, end_year + 1):
        data = year_func2(year)
        if data is not None and not data.empty:
            filtered2_data.append(data)
            years.append(year)
            Accidents.append(data["Accidents"].sum())
        else:
            st.write(f"No data found for year {year}")
    if len(filtered2_data) > 0:
        df_chart = pd.DataFrame({"Year": years, "Accidents": Accidents})
        chart = alt.Chart(df_chart).mark_line(point=True, color='red').encode(
            x=alt.X("Year:O", axis=alt.Axis(format='d', labelAngle=0, labelColor='black',
                                            titleColor='black', titleOpacity=1.0)),
            y=alt.Y("Accidents", axis=alt.Axis(labelColor='black',
                                               titleColor='black', titleOpacity=1.0)),
            tooltip=[alt.Tooltip('Year', title='Year'),
                     alt.Tooltip('Accidents', title='Accidents', format='d')]
        ).properties(
            width=850,
            height=700,
            title="Accident Count / Year"
        )
        st.altair_chart(chart)


# -------------------------
