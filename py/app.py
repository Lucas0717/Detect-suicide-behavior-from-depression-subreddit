# reddit posts datasets
from pmaw import PushshiftAPI
import pandas as pd
import calendar 
from datetime import datetime,timedelta
api = PushshiftAPI()
end_epoch = calendar.timegm(datetime.utcnow().utctimetuple())
start_epoch = calendar.timegm((datetime.utcnow()-timedelta(days=7)).utctimetuple())
submissions = api.search_submissions(subreddit="depression", after=start_epoch,before = end_epoch , mem_safe=True)
depression_df = pd.DataFrame(submissions)
keep_columns = ['author', 'author_fullname', 'subreddit', 'created_utc', 'full_link', 'num_comments', 'over_18', 'score', 'selftext', 'title']

new_depression_df = depression_df[keep_columns]
del depression_df

# remove punctuation and convert to lower case etc.
new_depression_df['tibo'] = new_depression_df['selftext'].astype(str) + new_depression_df['title'].astype(str)
new_depression_df['tibo'] = new_depression_df['tibo'].astype(str).str.replace('[^\w\s]','').str.lower().apply(lambda x: ' '.join([word for word in x.split() if word not in (stop)]))
new_depression_df = new_depression_df.astype(str).apply(lambda x: x.str.encode('ascii', 'ignore').str.decode('ascii'))
new_depression_df['tibo'] = new_depression_df['tibo'].str.replace('_', '').apply(lambda x: re.sub("\S*\d\S*", "", x).strip()) 
corpus4 = new_depression_df['tibo'].apply(lambda x: ' '.join(x)).str.replace(r"\s+(.)\1+\b", "").str.strip().tolist()

from datetime import datetime
def transfer_time(created_utc):
  return datetime.utcfromtimestamp(int(created_utc)).strftime("%Y-%m-%d %H:%M:%S")
new_depression_df['time'] = new_depression_df['created_utc'].apply(transfer_time)

# get count of day and count of hour
def transfer_day(date_time):
  new = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
  return new.strftime('%A')
def transfer_hour(date_time):
  new = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
  return new.strftime('%H')
my_date = new_depression_df['time'].to_frame()
my_date['day'] = my_date['time'].apply(transfer_day)
my_date['hour'] = my_date['time'].apply(transfer_hour)
count_day = my_date.groupby('day').size().to_frame()
count_day.columns = ['count']
count_day.index.name = None
count_hour = my_date.groupby('hour').size()
count_hour.columns = ['count']
count_hour.index.name = None
count_age = new_depression_df.groupby('over_18').size().to_frame()
count_age.columns = ['count']
count_age.index.name = None

import streamlit as st
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt

@st.cache(persist=True)#(If you have a different use case where the data does not change so very often, you can simply use this)
st.sidebar.checkbox("Show Analysis by time", True, key=1)
select = st.sidebar.selectbox('Select a State',df['state'])

#get the state selected in the selectbox
state_data = df[df['state'] == select]
select_status = st.sidebar.radio("Time status", ('Day','Hour', 'Age'))

def get_total_dataframe(dataset):
    total_dataframe = pd.DataFrame({
    'Status':['Confirmed', 'Recovered', 'Deaths','Active'],
    'Number of cases':(dataset.iloc[0]['confirmed'],
    dataset.iloc[0]['recovered'], 
    dataset.iloc[0]['deaths'],dataset.iloc[0]['active'])})
    return total_dataframe

state_total = get_total_dataframe(state_data)

if st.sidebar.checkbox("Show Analysis by State", True, key=2):
    st.markdown("## **State level analysis**")
    st.markdown("### Overall Confirmed, Active, Recovered and " + "Deceased cases in %s yet" % (select))
    if not st.checkbox('Hide Graph', False, key=1):
        state_total_graph = px.bar(
        state_total, 
        x='Status',
        y='Number of cases',
        labels={'Number of cases':'Number of cases in %s' % (select)},
        color='Status')
        st.plotly_chart(state_total_graph)