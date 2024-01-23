# YOU CAN FIND THE PROJECT BY COPY AND PASTING THIS LINK: https://calebs-projects-e4ylse8dl323i9smnynshk.streamlit.app/
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title("Sentiment Analysis of tweets about US Airline")
st.sidebar.title("Sentiment Analysis of tweets about US Airline")

st.markdown(" This application is a streamlit dashboard to analyze the sentiment of tweets \U0001f426")
st.markdown("Uncheck the Hide and Close boxes to see visuals")
st.sidebar.markdown(" This application is a streamlit dashboard to analyze the sentiment of tweets \U0001f426")

DATA_URL = ("Tweets.csv")

@st.cache_data()
def load_data():
    data = pd.read_csv(DATA_URL)
    data['tweet_created'] = pd.to_datetime(data['tweet_created'])
    return data

data = load_data()

st.sidebar.subheader("Show random tweet")
random_tweet = st.sidebar.radio('Sentiment', ('positive', 'neutral', 'negative'))
st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')[["text"]].sample(n=1).iat[0,0])

st.sidebar.markdown("### Number of tweets by sentiment")
select = st.sidebar.selectbox('Viusalization type', ['Bar Chart', 'Pie chart'], key='1')
sentiment_count = data['airline_sentiment'].value_counts()
sentiment_count = pd.DataFrame({'Sentiment':sentiment_count.index, 'Tweets':sentiment_count.values})

if not st.sidebar.checkbox("Hide", True):
    st.markdown("### Number of tweets by sentiment")
    if select == "Bar Chart":
        fig = px.bar(sentiment_count, x='Sentiment', y='Tweets', color='Sentiment', height=500)
        st.plotly_chart(fig)
    else:
        fig = px.pie(sentiment_count, values='Tweets', names='Sentiment')
        st.plotly_chart(fig)


st.sidebar.subheader("When and where are users tweeting from")
hour = st.sidebar.slider("Hour of day", 0, 23)
modified_data = data[data['tweet_created'].dt.hour == hour]
if not st.sidebar.checkbox("Close", True, key='2'):
    st.markdown("### Tweets locations based on the time of day")
    st.markdown("%i tweets between %i:00 and %i:00" % (len(modified_data), hour, (hour+1)%24))
    st.map(modified_data)
    if st.sidebar.checkbox("Show raw data", False):
        st.write(modified_data)


st.sidebar.subheader("Breakdown airline twees by sentiment")
choice = st.sidebar.multiselect('Pick airlines', ('US Airways', 'United', 'American', 'Southwest', 'Delta', 'Virgin America'), key='0')

if len(choice) > 0:
    choice_data = data[data.airline.isin(choice)]
    fig_choice = px.histogram(choice_data, x='airline', y='airline_sentiment', histfunc='count', color='airline_sentiment',
    facet_col='airline_sentiment', labels={'airline_sentiment':'tweets'}, height=600, width=800)
    st.plotly_chart(fig_choice)
