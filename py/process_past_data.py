from pmaw import PushshiftAPI
import pandas as pd
import calendar 
from sklearn.feature_extraction import text
from datetime import datetime,timedelta
import re

def get_depression_data():
    stop = text.ENGLISH_STOP_WORDS
    depression_data0 = pd.read_csv('./past_data/depression_data(2019.1.1-2019.9.29).csv',error_bad_lines=False, engine='python')
    depression_data1 = pd.read_csv('./past_data/depression_data(2019.9.30-2020.1.10).csv',error_bad_lines=False, engine='python')
    depression_data2 = pd.read_csv('./past_data/depression_data(2020.1.1-2020.6.10).csv',error_bad_lines=False, engine='python')
    depression_data3 = pd.read_csv('./past_data/depression_data(2020.6.11-2020.9.29).csv',error_bad_lines=False, engine='python')
    depression_data4 = pd.read_csv('./past_data/depression_data(2020.9.30-2021.4.30).csv',error_bad_lines=False, engine='python')
    depression_data5 = pd.read_csv('./past_data/depression_data(2021.5.1-2021.9.30).csv',error_bad_lines=False, engine='python')
    depression_data = pd.concat([depression_data0, depression_data1, depression_data2, depression_data3, depression_data4,depression_data5])
    depression_data = depression_data.drop(depression_data.columns[0], axis=1)
    depression_data.columns = ['author', 'author_fullname', 'created_utc', 'full_link', 'num_comments', 'over_18', 'score', 'selftext','subreddit', 'title']

    # remove punctuation and convert to lower case etc.
    new_depression_df = depression_data.dropna(how = 'any')

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
    
    new_depression_1 = new_depression_df[new_depression_df['time']<= "2020-03-01"]
    new_depression_2 = new_depression_df[new_depression_df['time']> "2020-03-01"]
    
    del new_depression_df

    my_date = new_depression_1['time'].to_frame()
    my_date['day'] = my_date['time'].apply(transfer_day)
    my_date['hour'] = my_date['time'].apply(transfer_hour)
    count_day = my_date.groupby('day').size().to_frame()
    count_day.columns = ['count']
    count_day.index.name = None
    count_hour = my_date.groupby('hour').size()
    count_hour.columns = ['count']
    count_hour.index.name = None
    count_age = new_depression_1.groupby('over_18').size().to_frame()
    count_age.columns = ['count']
    count_age.index.name = None
    count_day.to_csv('./before_pandemic/day_count_dep.csv')    
    count_hour.to_csv('./before_pandemic/hour_count_dep.csv')   
    count_age.to_csv('./before_pandemic/age_count_dep.csv')
    new_depression_1['tibo'].to_csv('./before_pandemic/depression.csv')


    my_date = new_depression_2['time'].to_frame()
    my_date['day'] = my_date['time'].apply(transfer_day)
    my_date['hour'] = my_date['time'].apply(transfer_hour)
    count_day = my_date.groupby('day').size().to_frame()
    count_day.columns = ['count']
    count_day.index.name = None
    count_hour = my_date.groupby('hour').size()
    count_hour.columns = ['count']
    count_hour.index.name = None
    count_age = new_depression_2.groupby('over_18').size().to_frame()
    count_age.columns = ['count']
    count_age.index.name = None
    count_day.to_csv('./after_pandemic/day_count_dep.csv')    
    count_hour.to_csv('./after_pandemic/hour_count_dep.csv')   
    count_age.to_csv('./after_pandemic/age_count_dep.csv')
    new_depression_2['tibo'].to_csv('./after_pandemic/depression.csv')


def get_suicide_data():
    stop = text.ENGLISH_STOP_WORDS
    suicide_data = pd.read_csv('./past_data/suicide_data.csv', encoding="unicode_escape")
    suicide_data.columns = ['author', 'author_fullname', 'created_utc', 'full_link', 'num_comments', 'over_18', 'score', 'selftext','subreddit', 'title']
    new_suicide_df = suicide_data.dropna(how = 'any')

    # remove punctuation and convert to lower case etc.
    new_suicide_df['tibo'] = new_suicide_df['selftext'].astype(str) + new_suicide_df['title'].astype(str)
    new_suicide_df['tibo'] = new_suicide_df['tibo'].astype(str).str.replace('[^\w\s]','').str.lower().apply(lambda x: ' '.join([word for word in x.split() if word not in (stop)]))
    new_suicide_df = new_suicide_df.astype(str).apply(lambda x: x.str.encode('ascii', 'ignore').str.decode('ascii'))
    new_suicide_df['tibo'] = new_suicide_df['tibo'].str.replace('_', '').apply(lambda x: re.sub("\S*\d\S*", "", x).strip()) 

    def transfer_time(created_utc):
        return datetime.utcfromtimestamp(int(float(created_utc))).strftime("%Y-%m-%d %H:%M:%S")
    new_suicide_df['time'] = new_suicide_df['created_utc'].apply(transfer_time)

    new_suicide_1 = new_suicide_df[new_suicide_df['time']<= "2020-03-01"]
    new_suicide_2 = new_suicide_df[new_suicide_df['time']> "2020-03-01"]

    del new_suicide_df
    # get count of day and count of hour
    def transfer_day(date_time):
        new = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
        return new.strftime('%A')
    def transfer_hour(date_time):
        new = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
        return new.strftime('%H')

    my_date = new_suicide_1['time'].to_frame()
    my_date['day'] = my_date['time'].apply(transfer_day)
    my_date['hour'] = my_date['time'].apply(transfer_hour)
    count_day = my_date.groupby('day').size().to_frame()
    count_day.columns = ['count']
    count_day.index.name = None
    count_hour = my_date.groupby('hour').size()
    count_hour.columns = ['count']
    count_hour.index.name = None
    count_age = new_suicide_1.groupby('over_18').size().to_frame()
    count_age.columns = ['count']
    count_age.index.name = None
    count_day.to_csv('./before_pandemic/day_count_sui.csv')    
    count_hour.to_csv('./before_pandemic/hour_count_sui.csv')    
    count_age.to_csv('./before_pandemic/age_count_sui.csv')
    new_suicide_1['tibo'].to_csv('./before_pandemic/suicide.csv')

    my_date = new_suicide_2['time'].to_frame()
    my_date['day'] = my_date['time'].apply(transfer_day)
    my_date['hour'] = my_date['time'].apply(transfer_hour)
    count_day = my_date.groupby('day').size().to_frame()
    count_day.columns = ['count']
    count_day.index.name = None
    count_hour = my_date.groupby('hour').size()
    count_hour.columns = ['count']
    count_hour.index.name = None
    count_age = new_suicide_2.groupby('over_18').size().to_frame()
    count_age.columns = ['count']
    count_age.index.name = None
    count_day.to_csv('./after_pandemic/day_count_sui.csv')    
    count_hour.to_csv('./after_pandemic/hour_count_sui.csv')    
    count_age.to_csv('./after_pandemic/age_count_sui.csv')
    new_suicide_2['tibo'].to_csv('./after_pandemic/suicide.csv')

if __name__ == "__main__":
    get_depression_data()
    get_suicide_data()
    #with open('./past_data/depression_data.csv') as f:
    #    print(f)