import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import date
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go

# Set the start date for the stock data
START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

# Streamlit app title
st.title('Stock Forecast App')

# List of stock options
stocks = ('GOOG', 'AAPL', 'MSFT', 'GME')
selected_stock = st.selectbox('Select dataset for prediction', stocks)

# Slider for number of years of prediction
n_years = st.slider('Years of prediction:', 1, 4)
period = n_years * 365

# Function to load the stock data
@st.cache
def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data

# Display loading message
data_load_state = st.text('Loading data...')
data = load_data(selected_stock)
data_load_state.text('Loading data... done!')

# Show the raw data
st.subheader('Raw data')
st.write(data.tail())

# Plot raw stock data (open and close prices)
def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
    fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

plot_raw_data()

# Prepare data for prediction
df_train = data[['Date', 'Close']]
df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

# Ensure 'y' is numeric
df_train['y'] = pd.to_numeric(df_train['y'], errors='coerce')

# Train the model using Prophet
m = Prophet()
m.fit(df_train)

# Predict future values
future = m.make_future_dataframe(periods=period)
forecast = m.predict(future)

# Display the forecasted data
st.subheader('Forecast data')
st.write(forecast.tail())

# Plot the forecast using Plotly
st.write(f'Forecast plot for {n_years} years')
fig1 = plot_plotly(m, forecast)
st.plotly_chart(fig1)

# Show the forecast components
st.write("Forecast components")
fig2 = m.plot_components(forecast)
st.write(fig2)
