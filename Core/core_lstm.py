import streamlit as st
import yfinance as yf
import torch
import torch.nn as nn
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import plotly.graph_objs as go

num_epochs = 100 # no of complete pass during the training process
time_step = 10


def fetch_and_prepare_data(ticker):
    data = yf.download(ticker, start='2020-01-01', end='2024-09-24')
    prices = data['Close'].values.reshape(-1, 1)

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_prices = scaler.fit_transform(prices)

    return scaled_prices, scaler, data


def create_dataset(data, time_step=1):  #time_step= no of previous time or trading days
    X, Y = [], []
    for i in range(len(data) - time_step - 1):
        X.append(data[i:(i + time_step), 0])
        Y.append(data[i + time_step, 0])
    return np.array(X), np.array(Y)


def train_model(X, y):
    X = torch.FloatTensor(X).view(-1, time_step)
    y = torch.FloatTensor(y)

    dataset = torch.utils.data.TensorDataset(X, y)
    #batch_size- no of sample to be precessed during iteration, shuffle- shuffle the dataset before epochs

    train_loader = torch.utils.data.DataLoader(dataset, batch_size=32, shuffle=True)

    model = nn.Linear(time_step, 1)
    criterion = nn.MSELoss()  #Mean Squared error loss
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001) #Loss function- Mean squared error

    for epoch in range(num_epochs):
        for inputs, labels in train_loader:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs.view(-1), labels)
            loss.backward()
            optimizer.step()

    return model


def forecast_prices(model, last_sequence):
    predictions = []
    for _ in range(252):  # Forecasting for 252 trading days
        with torch.no_grad():
            input_seq = torch.FloatTensor(last_sequence).view(1, time_step)
            next_price = model(input_seq).item()
            predictions.append(next_price)
            last_sequence = np.append(last_sequence[0][1:], next_price).reshape(1, -1)

    return predictions


def plot_technical_indicators_forecast(stock_data, forecast, stock_symbol, stock_name):
    df = stock_data.copy()

    fig = go.Figure()

    last_date = df.index[-1]
    forecast_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=len(forecast), freq='B')

    # Add forecast to the figure
    fig.add_trace(go.Scatter(x=forecast_dates, y=forecast, mode='lines', name='Forecast', line=dict(dash='dash')))
    #fig.add_trace(
    #    go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Historical Prices', line=dict(color='blue')))

    fig.update_layout(
        title=f'Stock Price with Technical Indicators for {stock_symbol} ({stock_name})',
        xaxis_title='Date (~1 Year)',
        yaxis_title='Price'
    )

    return fig


def init(stock_name):
    scaled_prices, scaler, data = fetch_and_prepare_data(stock_name)

    # Number of previous days to consider
    X, y = create_dataset(scaled_prices, time_step)

    model = train_model(X, y)

    last_sequence = scaled_prices[-time_step:].reshape(1, -1)
    predictions = forecast_prices(model, last_sequence)
    predicted_prices = scaler.inverse_transform(np.array(predictions).reshape(-1, 1))

    # Plotting with technical indicators and forecast
    fig = plot_technical_indicators_forecast(data, predicted_prices.flatten(), stock_name, stock_name)
    st.plotly_chart(fig)
