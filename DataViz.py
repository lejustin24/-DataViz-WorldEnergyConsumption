from cmath import pi
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from streamlit_modal import Modal
import streamlit.components.v1 as components

st.header('World Energy Consumption Dashboard')
st.markdown('''The world is shifting to more sustainable and clean forms of energy. It's critical to understand how energy consumption is now distributed throughout the world in order to pinpoint possibilities for improvement and expansion. We will examine the present situation of global energy use in this dashboard to demonstrate that renewable energy sources have a promising future as a viable alternative to non-renewable energy sources.''')
st.write('\n')
st.markdown("""---""")
st.caption('Data source: https://www.kaggle.com/datasets/pralabhpoudel/world-energy-consumption')
st.caption('**Note that for some graphs, you should select the right country and/or year.**')
st.markdown("""---""")
# Loading the dataset (csv file)
df = pd.read_csv('WorldEnergyConsumption.csv')

df['year'] = df['year'].astype(int) # make year col int
df = df.set_index('year') # make year col the index, we can also do it while loading the dataset with read_csv('', set_index='year')

# Create a new column for the total energy production
df['total_energy_prod_twh'] = df['coal_prod_change_twh'] + df['gas_prod_change_twh'] + df['oil_prod_change_twh'] + df['biofuel_electricity'] + df['nuclear_electricity'] + df['hydro_electricity'] + df['solar_electricity'] + df['wind_electricity']

# Create a new column for the total energy consumption
df['total_energy_cons_twh'] = df['energy_cons_change_twh'] + df['biofuel_cons_change_twh'] + df['coal_cons_change_twh'] + df['gas_cons_change_twh'] + df['nuclear_cons_change_twh'] + df['hydro_cons_change_twh'] + df['oil_cons_change_twh'] + df['other_renewables_cons_change_twh']

# Create a new column for the total renewable energy production
df['total_renewables_prod_twh'] = df['biofuel_electricity'] + df['hydro_electricity'] + df['solar_electricity'] + df['wind_electricity'] + df['other_renewable_exc_biofuel_electricity']

# Create a new column for the total renewable energy consumption
df['total_renewables_cons_twh'] = df['biofuel_cons_change_twh'] + df['hydro_cons_change_twh'] + df['solar_cons_change_twh'] + df['wind_cons_change_twh'] + df['other_renewables_cons_change_twh']

# Sidebar - energy type selection
st.sidebar.subheader('Energy type')
energy_type = st.sidebar.selectbox('Select energy type', ['Coal', 'Oil', 'Gas', 'Biofuel', 'Nuclear', 'Hydro', 'Solar', 'Wind', 'Renewables', 'Other renewables'])

# Chart 1: Scatter plot of total energy consumption vs. total renewable energy consumption
st.subheader('Scatter plot of total energy consumption vs. total renewable energy consumption by country')
fig = px.scatter(df, x='total_energy_cons_twh', y='total_renewables_cons_twh', color='country', hover_name='country', log_x=True, log_y=True, size_max=60)
st.plotly_chart(fig)

# Chart 2: Bar chart of total energy production by country
st.subheader('Bar chart of total energy production by country')
fig = px.bar(df, x='country', y='total_energy_prod_twh', color='country', hover_name='country', log_y=True)
st.plotly_chart(fig)

# Chart 3: Bar chart of total energy consumption by country
st.subheader('Bar chart of total energy consumption by country')
fig = px.bar(df, x='country', y='total_energy_cons_twh', color='country', hover_name='country', log_y=True)
st.plotly_chart(fig)

def chart4(country):
    df_country = df[df['country'] == country]
    chart4_data = df_country[['coal_prod_change_twh', 'oil_prod_change_twh', 'gas_prod_change_twh', 'biofuel_electricity', 'nuclear_electricity', 'hydro_electricity', 'solar_electricity', 'wind_electricity', 'coal_cons_change_twh', 'oil_cons_change_twh', 'gas_cons_change_twh', 'biofuel_cons_change_twh', 'nuclear_cons_change_twh', 'hydro_cons_change_twh', 'solar_cons_change_twh', 'wind_cons_change_twh']].reset_index()
    chart4_data = pd.melt(chart4_data, id_vars=['year'], var_name='type', value_name='twh')
    chart4 = alt.Chart(chart4_data).mark_line().encode(
    x='year',
    y='twh',
    color='type'
    ).properties(
    width=700,
    height=400,
    title=f'Energy production and consumption over time for {country}'
    )
    return chart4

st.sidebar.subheader('Country')
country = st.sidebar.selectbox('Select a country', df['country'].unique())
st.write(f'## Energy production and consumption over time for {country}')
st.altair_chart(chart4(country), use_container_width=True)
selected_country = country

def chart5(year):
    df_year = df[df.index == year]
    chart5_data = df_year[['coal_cons_change_twh', 'oil_cons_change_twh', 'gas_cons_change_twh', 'biofuel_cons_change_twh', 'nuclear_cons_change_twh', 'hydro_cons_change_twh', 'solar_cons_change_twh', 'wind_cons_change_twh']].reset_index()
    chart5_data = pd.melt(chart5_data, id_vars=['year'], var_name='type', value_name='twh')
    chart5 = alt.Chart(chart5_data).mark_bar().encode(
    x='twh',
    y=alt.Y('type', sort='-x'),
    color='type'
    ).properties(
    width=700,
    height=400,
    title=f'Energy consumption by energy type in {year}'
    )
    return chart5

st.sidebar.subheader('Year')
year = st.sidebar.slider('Select year', 1900, 2020)
st.write(f'## Energy consumption by energy type in {year}')
st.altair_chart(chart5(year), use_container_width=True)
selected_year = year

# Callback to update scatter plot based on selected year
@st.cache_data
def update_scatter_plot(year):
    scatter_data = df[df.index == year][['total_energy_cons_twh', 'total_renewables_cons_twh', 'country']]
    scatter_data = scatter_data.dropna()
    fig = px.scatter(scatter_data, x='total_energy_cons_twh', y='total_renewables_cons_twh', color='country', hover_name='country', log_x=True, log_y=True, size_max=60)
    fig.update_layout(title=f'Total energy consumption vs. total renewable energy consumption ({year})')
    return fig

#there was a duplicate of this code, so I commented it out
# scatter_fig = update_scatter_plot(selected_year)
# st.plotly_chart(scatter_fig)

# Update scatter plot based on selected year
# if scatter_fig:
scatter_fig = update_scatter_plot(selected_year)
scatter_fig.update_layout(title=f'Total energy consumption vs. total renewable energy consumption ({selected_year})')
st.plotly_chart(scatter_fig)


# Chart 6: Stacked bar chart of energy production and consumption by year for the selected country
st.subheader(f'Energy production and consumption in {selected_country}')
df_country = df.loc[df['country'] == selected_country, ['total_energy_prod_twh', 'total_energy_cons_twh']].reset_index()
df_country_melted = pd.melt(df_country, id_vars=['year'], value_vars=['total_energy_prod_twh', 'total_energy_cons_twh'], var_name='type', value_name='twh')
chart6 = alt.Chart(df_country_melted).mark_bar().encode(
    x=alt.X('year', axis=alt.Axis(format='f')),
    y=alt.Y('twh', axis=alt.Axis(title='TWh')),
    color='type',
    tooltip=['year', 'twh']
).properties(
    width=700,
    height=400
).configure_legend(orient='top')
st.altair_chart(chart6, use_container_width=True)


chart8_data = df[['total_renewables_prod_twh', 'total_renewables_cons_twh']].reset_index()
chart8_data = pd.melt(chart8_data, id_vars=['year'], var_name='type', value_name='twh')
chart8 = alt.Chart(chart8_data).mark_line().encode(
x='year',
y='twh',
color='type'
).properties(
width=700,
height=400,
title='Total renewable energy production and consumption over time'
)
st.altair_chart(chart8, use_container_width=True)

df_country_cons = df.groupby('country')['total_energy_cons_twh'].sum().reset_index()

# choropleth map
st.subheader(f'Map of total energy consumption by country')
chart9 = px.choropleth(df_country_cons, locations='country', locationmode='country names', color='total_energy_cons_twh', projection='natural earth')
st.plotly_chart(chart9)

df_energy_changes = df[['coal_prod_change_pct',
 'gas_prod_change_pct',
 'oil_prod_change_pct',
 'biofuel_share_elec',
 'carbon_intensity_elec',
 'coal_share_elec',
 'gas_share_elec',
 'hydro_share_elec',
 'low_carbon_share_elec',
 'nuclear_share_elec',
 'oil_share_elec',
 'other_renewables_share_elec',
 'renewables_share_elec',
 'solar_share_elec',
 'wind_share_elec']]

st.subheader(f'Heatmap of energy production and consumption changes')
chart10 = px.imshow(df_energy_changes.corr())
st.plotly_chart(chart10)

df_renewables = df.groupby('country')['renewables_cons_change_twh'].sum().reset_index()
st.subheader(f'Treemap of renewable energy consumption by country')
chart11 = px.treemap(df_renewables, path=['country'], values='renewables_cons_change_twh')
st.plotly_chart(chart11)


st.subheader(f'Polar chart of energy production and consumption in {selected_country}')
chart12 = px.line_polar(df_country, r='total_energy_prod_twh', theta='year', line_close=True)
chart13 = px.line_polar(df_country, r='total_energy_cons_twh', theta='year', line_close=True)
st.plotly_chart(chart12)
st.plotly_chart(chart13)

st.subheader(f'Box plot of energy production and consumption in {selected_country}')
chart14 = px.box(df_country, x='year', y='total_energy_prod_twh')
chart15 = px.box(df_country, x='year', y='total_energy_cons_twh')
st.plotly_chart(chart14)
st.plotly_chart(chart15)

# treemap of oil production by country
df_oil = df.groupby('country')['oil_prod_change_pct'].sum().reset_index()
st.subheader(f'Treemap of oil production by country')
chart16 = px.treemap(df_oil, path=['country'], values='oil_prod_change_pct')
st.plotly_chart(chart16)

# gauge chart of renewable consumption by country
df_renewables = df.groupby('country')['other_renewable_consumption'].sum().reset_index()
st.subheader(f'Gauge chart of renewable consumption in {selected_country}')
fig = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = df_renewables[df_renewables['country'] == selected_country]['other_renewable_consumption'].values[0],
    title = {'text': "Gauge Chart"},
    domain = {'x': [0, 1], 'y': [0, 1]},
    gauge = {
        'axis': {'range': [None, df_renewables['other_renewable_consumption'].max()]},
        'bar': {'color': "darkblue"},
        'steps' : [
            {'range': [0, df_renewables['other_renewable_consumption'].max()/3], 'color': 'lightgray'},
            {'range': [df_renewables['other_renewable_consumption'].max()/3, df_renewables['other_renewable_consumption'].max()*2/3], 'color': 'gray'},
            {'range': [df_renewables['other_renewable_consumption'].max()*2/3, df_renewables['other_renewable_consumption'].max()], 'color': 'darkgray'}],
        'threshold': {
            'line': {'color': "red", 'width': 4},
            'thickness': 0.75,
            'value': df_renewables['other_renewable_consumption'].max()/2}}))

st.plotly_chart(fig)

st.markdown('''The usage of renewable energy has grown over time, and there is substantial room for expansion moving forward.The energy source that is consumed the most globally is oil, the remaining energy consumption was primarily made up of renewable energy sources. The graphs in this dashboard show the necessity of switching to renewable energy sources in order to lower carbon dioxide emissions and lessen the impact of climate change.''')