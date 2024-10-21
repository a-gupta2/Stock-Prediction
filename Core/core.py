from statsmodels.tsa.holtwinters import ExponentialSmoothing
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import plotly.graph_objs as go
import pandas as pd


def forecast_stock(stock_data):
    """Forecast future stock prices using Holt-Winters Exponential Smoothing."""
    df = stock_data[['Close']]
    model = ExponentialSmoothing(df['Close'], trend='add', seasonal='add', seasonal_periods=252)
    fit = model.fit()

    forecast = fit.forecast(steps=252)
    return forecast


def plot_technical_indicators_forecast(stock_data, forecast, stock_symbol, stock_name):
    """Plot RSI, Bollinger Bands, SMA, and forecast with the stock name and symbol."""

    # Ensure the 'Date' column is in datetime format and set as index
    df = stock_data.copy()

    fig = go.Figure()

    # Create forecast dates and ensure they are correct
    last_date = df.index[-1]
    forecast_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=len(forecast), freq='B')

    # Add forecast to the figure
    fig.add_trace(go.Scatter(x=forecast_dates, y=forecast, mode='lines', name='Forecast', line=dict(dash='dash')))

    # Set the graph title with the stock symbol and name
    fig.update_layout(
        title=f'Stock Price with Technical Indicators for {stock_symbol} ({stock_name})',
        xaxis_title='Date (~1 Year)',
        yaxis_title='Price'
    )

    return fig


def plot_technical_indicators_actual(stock_data, stock_symbol, stock_name):
    """Plot RSI, Bollinger Bands, SMA, and forecast with the stock name and symbol."""

    # Ensure the 'Date' column is in datetime format and set as index
    stock_data['Date'] = pd.to_datetime(stock_data['Date'])
    stock_data.set_index('Date', inplace=True)

    df = stock_data.copy()

    # Calculate RSI
    delta = df['Close'].diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # Calculate Bollinger Bands and SMA
    df['SMA'] = df['Close'].rolling(window=20).mean()
    df['STD'] = df['Close'].rolling(window=20).std()
    df['Upper Band'] = df['SMA'] + (df['STD'] * 2)
    df['Lower Band'] = df['SMA'] - (df['STD'] * 2)

    fig = go.Figure()

    # Plot the Close Price and Technical Indicators
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Close Price'))
    fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], mode='lines', name='RSI'))
    fig.add_trace(go.Scatter(x=df.index, y=df['Upper Band'], mode='lines', name='Upper Band'))
    fig.add_trace(go.Scatter(x=df.index, y=df['Lower Band'], mode='lines', name='Lower Band'))

    # Set the graph title with the stock symbol and name
    fig.update_layout(
        title=f'Stock Price with Technical Indicators for {stock_symbol} ({stock_name})',
        xaxis_title='Date (Jan-1996 to Sep-2024)',
        yaxis_title='Price'
    )

    return fig


def analyze_sentiment(articles):
    if articles.empty:
        print("The articles DataFrame is empty.")
        return pd.DataFrame()

    if 'description' in articles.columns and articles['description'].notna().any():
        texts = articles["description"].tolist()  # Use description if available
    elif 'title' in articles.columns:
        texts = articles["title"].tolist()  # Fallback to title if description is not available
    else:
        print("Neither 'description' nor 'title' columns are available in the articles DataFrame.")
        return pd.DataFrame()  # Return an empty DataFrame

    texts = [text for text in texts if isinstance(text, str) and text.strip()]

    if not texts:  # Check if the list is empty
        print("The selected text list is empty or contains only non-string entries.")
        return pd.DataFrame()  # Return an empty DataFrame

    analyzer = SentimentIntensityAnalyzer()

    sentiments = [analyzer.polarity_scores(text) for text in texts]

    sentiments_df = pd.DataFrame(sentiments)

    return sentiments_df
