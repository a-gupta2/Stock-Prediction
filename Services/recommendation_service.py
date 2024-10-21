import plotly.graph_objects as go
import streamlit as st

def plot_recommendation(average_sentiment_score):
    # Update the thresholds based on the provided logic
    thresholds = {
        'Buy': 0.3,
        'Hold': -0.3,
        'Sell': -1.0
    }

    # Determine the recommendation based on the sentiment score
    if average_sentiment_score >= thresholds['Buy']:
        recommendation = 'Buy'
    elif average_sentiment_score >= thresholds['Hold']:
        recommendation = 'Hold'
    else:
        recommendation = 'Sell'

    # Create a speedometer chart
    fig = go.Figure()

    # Add a gauge trace
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=average_sentiment_score,
        title={'text': "Sentiment Score", 'font': {'size': 10}},
        gauge={
            'axis': {'range': [-1, 1]},
            'bar': {'color': "blue"},
            'steps': [
                {'range': [-1, -0.3], 'color': "lightcoral"},  # Sell
                {'range': [-0.3, 0.3], 'color': "orange"},     # Hold
                {'range': [0.3, 1], 'color': "lightgreen"},    # Buy
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.55,
                'value': average_sentiment_score
            }
        }
    ))

    # Update layout
    fig.update_layout(height=200, margin=dict(l=20, r=20, t=20, b=20))

    # Display the speedometer chart
    st.plotly_chart(fig)

    # Display the overall recommendation
    st.subheader("Overall Recommendation:")
    st.write(f"The average sentiment score is **{average_sentiment_score:.2f}**, leading to a recommendation of: **{recommendation}**")
