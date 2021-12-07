import pandas as pd
from datetime import datetime,timedelta
import re
from sklearn.feature_extraction import text

def get_depression_data():
    stop = text.ENGLISH_STOP_WORDS
    new_depression_df = pd.read_csv('/past_data/depression_data(2020.9.30-2021.9.30).csv')

    # remove punctuation and convert to lower case etc.
    new_depression_df['tibo'] = new_depression_df['selftext'].astype(str) + new_depression_df['title'].astype(str)
    new_depression_df['tibo'] = new_depression_df['tibo'].astype(str).str.replace('[^\w\s]','').str.lower().apply(lambda x: ' '.join([word for word in x.split() if word not in (stop)]))
    new_depression_df = new_depression_df.astype(str).apply(lambda x: x.str.encode('ascii', 'ignore').str.decode('ascii'))
    new_depression_df['tibo'] = new_depression_df['tibo'].str.replace('_', '').apply(lambda x: re.sub("\S*\d\S*", "", x).strip()) 

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
    count_day.to_csv('/past_data/day_count_dep.csv')    
    count_hour.to_csv('/past_data/hour_count_dep.csv')    
    count_age.to_csv('/past_data/age_count_dep.csv')
    new_depression_df.to_csv('/past_data/depression.csv')

def get_suicide_data():
    stop = text.ENGLISH_STOP_WORDS
    new_suicide_df = pd.read_csv('./past_data/suicide_data.csv',  encoding= 'unicode_escape')

    # remove punctuation and convert to lower case etc.
    new_suicide_df['tibo'] = new_suicide_df['selftext'].astype(str) + new_suicide_df['title'].astype(str)
    new_suicide_df['tibo'] = new_suicide_df['tibo'].astype(str).str.replace('[^\w\s]','').str.lower().apply(lambda x: ' '.join([word for word in x.split() if word not in (stop)]))
    new_suicide_df = new_suicide_df.astype(str).apply(lambda x: x.str.encode('ascii', 'ignore').str.decode('ascii'))
    new_suicide_df['tibo'] = new_suicide_df['tibo'].str.replace('_', '').apply(lambda x: re.sub("\S*\d\S*", "", x).strip()) 
    new_suicide_df = new_suicide_df.dropna(axis=0)

    def transfer_time(created_utc):
        return datetime.utcfromtimestamp(int(float(created_utc))).strftime("%Y-%m-%d %H:%M:%S")
    new_suicide_df['time'] = new_suicide_df['created_utc'].apply(transfer_time)

    # get count of day and count of hour
    def transfer_day(date_time):
        new = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
        return new.strftime('%A')
    def transfer_hour(date_time):
        new = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
        return new.strftime('%H')
    my_date = new_suicide_df['time'].to_frame()
    my_date['day'] = my_date['time'].apply(transfer_day)
    my_date['hour'] = my_date['time'].apply(transfer_hour)
    count_day = my_date.groupby('day').size().to_frame()
    count_day.columns = ['count']
    count_day.index.name = None
    count_hour = my_date.groupby('hour').size()
    count_hour.columns = ['count']
    count_hour.index.name = None
    count_age = new_suicide_df.groupby('over_18').size().to_frame()
    count_age.columns = ['count']
    count_age.index.name = None
    count_day.to_csv('./past_data/day_count_sui.csv')    
    count_hour.to_csv('./past_data/hour_count_sui.csv')    
    count_age.to_csv('./past_data/age_count_sui.csv')
    new_suicide_df.to_csv('./past_data/suicide.csv')

if __name__ == "__main__":
    #get_depression_data()
    get_suicide_data()