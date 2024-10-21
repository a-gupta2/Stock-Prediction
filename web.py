from Services.news_service import *
from Services.recommendation_service import *
from Services.stock_service import *
from Core.core import *
from helper import *
from Core.core_lstm import init as lstm


def init():
    # 1. Title of the app
    st.set_page_config(layout="wide")
    st.markdown("<h1 style='text-align: center;'>Stocks Dashboard</h1>", unsafe_allow_html=True)

    # 2. Load configuration
    config = load_config()
    news_api_key = config.get('news_api_key')
    news_url = config.get('news_url')
    start_date = config.get('start_date')
    get_stocks_url = config.get('get_stocks_url')

    # 2. Dropdown to select a company
    stocks = get_sp500_stocks(get_stocks_url)
    company_list = [(row['Security'], row['Symbol']) for _, row in stocks.iterrows()]
    selected_company = st.selectbox("Select a Company (S&P 500 companies):", company_list)

    selected_company_name, selected_company_symbol = selected_company

    # 3. Display the selected company name
    st.markdown(f"<span style='color:red;'>**Company Name:** {selected_company_name}</span>", unsafe_allow_html=True)

    # 4. Create tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["Overview", "Chart", "Forecast", "Recommendation", "News"])

    # 5. Get stock data from yf
    stock_all_data = get_stock_data_from_yf(selected_company_symbol, start_date)

    stock_data = stock_all_data[['Date', 'Close']]

    #6. Overview
    with tab1:
        with st.spinner("Fetching stocks fundamentals.."):
            stock_fundamentals = get_stock_fundamentals(selected_company_symbol)
            fundamentals = stock_fundamentals
            fundamentals_df = pd.DataFrame(fundamentals.items(), columns=["Metric", "Value"])
            st.dataframe(fundamentals_df, hide_index=True)

    with tab2:  # Chart
        with st.spinner("Loading Chart..."):
            fig = plot_technical_indicators_actual(stock_data, selected_company_name, selected_company_symbol)
            st.plotly_chart(fig)

    with tab3:  # Projection
        model_selection = st.selectbox(
            "Select Projection Model",
            options=["Exponential Smoothing", "LSTM"]
        )

        with st.spinner("Loading Forecast chart..."):
            if model_selection == "Exponential Smoothing":  # Exponential Smoothing
                # Model: Exponential Smoothing
                forecast = forecast_stock(stock_data)
                fig = plot_technical_indicators_forecast(stock_data, forecast, selected_company_name,
                                                         selected_company_symbol)
                st.plotly_chart(fig)
            elif model_selection == "LSTM":  # Forecast-LSTM
                # Model: LSTM
                lstm(selected_company_symbol)

    with tab4:  # recommendation
        with st.spinner("Analysing market sentiments.."):
            articles = get_latest_stock_news(news_url, news_api_key, selected_company_symbol)

            sentiment = analyze_sentiment(articles)
            sentiment_scores = sentiment

            # Calculate the average compound sentiment score
            average_sentiment_score = sentiment_scores['compound'].mean()

            # Plot recommendation
            plot_recommendation(average_sentiment_score)

    with tab5:  # News
        with st.spinner("Fetching latest stock news.."):
            news_articles = get_latest_stock_news(news_url, news_api_key, selected_company_symbol)

            if not news_articles.empty:
                for index, article in news_articles.iterrows():
                    st.markdown(
                        f"<li><strong>{article['title']}</strong>: {article['description']} (<a href='{article['url']}'>Read more</a>)</li>",
                        unsafe_allow_html=True
                    )
            else:
                st.write("No news articles available.")
