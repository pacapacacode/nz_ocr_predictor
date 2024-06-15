import streamlit as st
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime
import plotly.graph_objs as go
import plotly.express as px

st.title("Official Cash Rate Prediction App")

# Load historic data
historic_data = pd.read_csv("./data/historic_output.csv", header=0)

# Set date index
historic_data['Date'] = pd.to_datetime(historic_data['Date']).dt.date
historic_data.set_index('Date', inplace=True)

# Headings
st.header("Historical data")
st.subheader("Economic Indicators graph")

# Box selection and sliders
column_names = historic_data.columns.tolist()

y_axis = st.selectbox('Select a column for the y-axis', column_names)

date_range = st.slider('Select Date Range:', min_value = historic_data.index.min(), max_value = historic_data.index.max(), value = (historic_data.index.min(),historic_data.index.max()))

filtered_historic_data = historic_data[(historic_data.index >= date_range[0]) & (historic_data.index <= date_range[1])]

# Create a line chart
fig1 = px.line(filtered_historic_data, x=filtered_historic_data.index, y=y_axis)
st.plotly_chart(fig1)
# st.line_chart(filtered_historic_data, x='index', y=y_axis)

st.subheader("Economic indicators data table")
# Create a table
st.write(filtered_historic_data)
st.write("Source: RBNZ")

# Get OCR forecast data
ocr_forecasts = pd.read_csc("./data/predictions_base.csv", header=0)
ocr_forecasts.set_index('Date',inplace=True)

st.header("Forecasts")
st.subheader("Baseline forecast using RBNZ projections")

selected_columns = st.multiselect('Select forecasts', ocr_forecasts.columns)

fig2 = go.Figure()

for col in selected_columns:
    fig2.add_trace(go.Scatter(x=ocr_forecasts.index, y=ocr_forecasts[col], mode='lines', name=col))

st.plotly_chart(fig2, use_container_width=True)

# Scenario 1: Sticky inflation
predictions_sticky = pd.read_csv("./data/predictions_sticky.csv", header=0)
predictions_sticky['Date'] = pd.to_datetime(predictions_sticky['Date']).dt.date
predictions_sticky.set_index('Date', inplace=True)

st.subheader("Scenario 1: Persistent inflation for 6 quarters")

selected_columns2 = st.multiselect('Select forecasts', predictions_sticky.columns)

fig3 = go.Figure()

for col in selected_columns2:
    fig3.add_trace(go.Scatter(x=predictions_sticky.index, y=predictions_sticky[col], mode='lines', name=col))

st.plotly_chart(fig3, use_container_width=True)

# Scenario 2: Economic downturn
predictions_downturn = pd.read_csv("./data/predictions_downturn.csv", header=0)
predictions_downturn['Date'] = pd.to_datetime(predictions_downturn['Date']).dt.date
predictions_downturn.set_index('Date', inplace=True)

st.subheader("Scenario 2: Higher Unemployment and Lower GDP growth than expected for 6 quarters")


fig4 = go.Figure()

for col in selected_columns2:
    fig4.add_trace(go.Scatter(x=predictions_downturn.index, y=predictions_downturn[col], mode='lines', name=col))

st.plotly_chart(fig4, use_container_width=True)
st.write("Sources: RBNZ, ANZ, ASB")

st.header("Glossary")
st.subheader("Machine Learning Models")

model_glossary = {
    'Linear Regression': 'Linear Regression calculates the output by assigning a coefficient to each of the variables. It chooses the coefficients so that the overall predictive error is minimized. Conceptually, for a single predictor variable, you are fitting a line of best fit on the data.',
    'Decision Tree': 'A Decision Tree algorithm calculates the value through a series of Yes/No logic. It’s like playing a game of 20 questions. The algorithm asks a series of yes/no questions about the data until it can make a prediction.',
    'Random Forest': 'A Random Forest model randomly generates a number of decision trees and takes the average of their results.',
    'K Nearest Neighbors (KNN)': 'K Nearest Neighbors makes a prediction by taking the average result of a number of data points that are most similar to the data that you are trying to predict.',
    'Support Vector Regression (SVR)': 'Support Vector Regression makes predictions while trying to fit the error within a certain threshold'
}

# Create a selectbox for the terms
selected_term = st.selectbox('Select a term', options=list(model_glossary.keys()))

# Display the definition of the selected term
st.markdown(f'**{selected_term}**: {model_glossary[selected_term]}')

st.subheader("Economic Terms")

economic_glossary = {
    'Official Cash Rate (OCR)': 'The Official Cash Rate (OCR) in New Zealand is an interest rate set by the Reserve Bank of New Zealand. It defines the wholesale price of borrowed money and influences all other interest rates. This rate directly affects the commercial banks, determining the rates they offer their customers. The Reserve Bank uses the OCR to achieve and maintain price stability. To keep prices stable, the Government has set an inflation target between 1% and 3% over the medium term with a focus on the 2% midpoint. Increasing the OCR increases interest rates and helps bring inflation down.',
    'Consumer Price Index (CPI)': 'The CPI is a measure that examines the weighted average of prices of a basket of consumer goods and services, such as transportation, food, and medical care1. It is calculated by taking price changes for each item in the predetermined basket of goods and averaging them. CPI is the main measure used to measure inflation, the rate at which prices are increasing.',
    'House Price Index (HPI)': 'The HPI measures the price changes of residential properties. The HPI is a tool that measures changes in single-family home prices across the country.',
    'Gross Domestic Product (GDP)': 'GDP is the total monetary or market value of all the finished goods and services produced within a country\’s borders in a specific time period. It serves as a comprehensive scorecard of a given country\’s economic health',
    'Government Spending': 'Government spending refers to the money spent by the public sector on the acquisition of goods and provision of services such as education, healthcare, social protection, and defense3. In the calculation of GDP, government spending denotes expenditures on goods and services by the government. It is one of the components of GDP.',
    'Consumption': 'Consumption is defined as the use of goods and services by a household. It is a component in the calculation of the GDP. Macroeconomists typically use consumption as a proxy of the overall economy6. Consumer spending accounts for between half and two-thirds of GDP in most countries.',
    'Unemployment Rate': 'The Unemployment Rate is the percentage of unemployed individuals in an economy among individuals currently in the labour force. Here, unemployed individuals are those who are currently not working but are actively seeking work'

}

# Create a selectbox for the terms
selected_term = st.selectbox('Select a term', options=list(economic_glossary.keys()))

# Display the definition of the selected term
st.markdown(f'**{selected_term}**: {economic_glossary[selected_term]}')
