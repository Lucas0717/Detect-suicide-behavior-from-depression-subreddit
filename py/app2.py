import streamlit as st
import pandas as pd
import pandas as pd
from scrap_data import *
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from sklearn.feature_extraction.text import CountVectorizer
from predict_prob import *
import altair as alt

def set_intro():
    st.image('https://suicidepreventionlifeline.org/wp-content/uploads/2016/08/Ribbon-1.png', width= 100)
    st.markdown('<h2 style="text-align:center;color:black;font-weight:bolder;font-size:50px;">Detect Suicide Behavior In<br>Depression Subreddit</h2>',unsafe_allow_html=True)
    st.write('')
    st.subheader('Reddit is an American social news aggregation, web content rating, and discussion website. Reddit has subreddits for different topics. There are several subreddits related to mental health problems. ')
    st.subheader('Our team focus on depression and suicide behaviors. Major depression does increase suicide risk compared to people without depression, and the risk of suicide is somehow related to the severity of the depression. ')
    st.subheader('The project aims at using machine learning and data analysis techniques for posts from subreddits r/depression and r/suicide on Reddit. The team wants to take the posts on Depression subreddit seriously and help to prevent suicide.')
def set_data():
    st.markdown("<h1 style='text-align: center; color: black;'>Data Analysis</h1>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: right; color: black;'>Before Pandemic:2019.1.1-2020.3.1</h5>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: right; color: black;'>After Pandemic:2020.3.1-2021.9.30</h5>", unsafe_allow_html=True)
    menu = st.radio(
    "",
    (" Weekdays  Frequency ",
    " Time  Frequency ",
     " Age  Frequency ",
     " Word  Cloud "),)

    tick_size = 12
    axis_title_size = 16
    if menu == " Weekdays  Frequency ":
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader('Depression Datasets')
            st.markdown(' ')
            count_day = pd.read_csv('./before_pandemic/day_count_dep.csv')
            count_day.columns = ['day','count']
            cats = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            count_day = count_day.set_index('day').reindex(cats).reset_index()
            
            fig = alt.Chart(count_day).transform_joinaggregate(
                TotalTime='sum(count)',
            ).transform_calculate(
                PercentOfTotal="datum.count / datum.TotalTime"
            ).mark_bar(color="red", size=35).encode(
                alt.Y('PercentOfTotal:Q', axis=alt.Axis(format='.0%')),
                x=alt.X("day:N", title="Day",sort=None),
                tooltip=[
                        alt.Tooltip("PercentOfTotal:Q", title="PercentOfTotal",format='.2%'),
                    ],
            )
            fig = alt.layer(fig).configure_axis(
                labelFontSize=tick_size, titleFontSize=axis_title_size
            ).properties(title='Before pandemic')

            st.altair_chart(fig, use_container_width=True)
            
            
            st.subheader('Suicide Datasets')

            st.markdown(' ')
            count_day = pd.read_csv('./before_pandemic/day_count_sui.csv')
            count_day.columns = ['day','count']
            cats = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            count_day = count_day.set_index('day').reindex(cats).reset_index()

            fig = alt.Chart(count_day).transform_joinaggregate(
                TotalTime='sum(count)',
            ).transform_calculate(
                PercentOfTotal="datum.count / datum.TotalTime"
            ).mark_bar(color="red", size=35).encode(
                alt.Y('PercentOfTotal:Q', axis=alt.Axis(format='.0%')),
                x=alt.X("day:N", title="Day",sort=None),
                tooltip=[
                        alt.Tooltip("PercentOfTotal:Q", title="PercentOfTotal",format='.2%'),
                    ],
            )
        
            fig = alt.layer(fig).configure_axis(
                labelFontSize=tick_size, titleFontSize=axis_title_size
            ).properties(title='Before pandemic')
            st.altair_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader(' 　│')
            st.markdown(' ')
            count_day = pd.read_csv('./after_pandemic/day_count_dep.csv')
            count_day.columns = ['day','count']
            cats = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            count_day = count_day.set_index('day').reindex(cats).reset_index()
            
            fig = alt.Chart(count_day).transform_joinaggregate(
                TotalTime='sum(count)',
            ).transform_calculate(
                PercentOfTotal="datum.count / datum.TotalTime"
            ).mark_bar(color="green", size=35).encode(
                alt.Y('PercentOfTotal:Q', axis=alt.Axis(format='.0%')),
                x=alt.X("day:N", title="Day",sort=None),
                tooltip=[
                        alt.Tooltip("PercentOfTotal:Q", title="PercentOfTotal",format='.2%'),
                    ],
            )
            fig = alt.layer(fig).configure_axis(
                labelFontSize=tick_size, titleFontSize=axis_title_size
            ).properties(title='After pandemic')

            st.altair_chart(fig, use_container_width=True)
            
            
            st.subheader('　│')

            st.markdown(' ')
            count_day = pd.read_csv('./after_pandemic/day_count_sui.csv')
            count_day.columns = ['day','count']
            cats = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            count_day = count_day.set_index('day').reindex(cats).reset_index()
            
            fig = alt.Chart(count_day).transform_joinaggregate(
                TotalTime='sum(count)',
            ).transform_calculate(
                PercentOfTotal="datum.count / datum.TotalTime"
            ).mark_bar(color="green", size=35).encode(
                alt.Y('PercentOfTotal:Q', axis=alt.Axis(format='.0%')),
                x=alt.X("day:N", title="Day",sort=None),
                tooltip=[
                        alt.Tooltip("PercentOfTotal:Q", title="PercentOfTotal",format='.2%'),
                    ],
            )
            fig = alt.layer(fig).configure_axis(
                labelFontSize=tick_size, titleFontSize=axis_title_size
            ).properties(title='After pandemic')
            st.altair_chart(fig, use_container_width=True)
        with col3:
            
            st.subheader('　│')            
            st.markdown(' ')
            count_day = pd.read_csv('./past_7days/day_count_dep.csv')
            count_day.columns = ['day','count']
            cats = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            count_day = count_day.set_index('day').reindex(cats).reset_index()
            
            fig = alt.Chart(count_day).transform_joinaggregate(
                TotalTime='sum(count)',
            ).transform_calculate(
                PercentOfTotal="datum.count / datum.TotalTime"
            ).mark_bar(color="blue", size=35).encode(
                alt.Y('PercentOfTotal:Q', axis=alt.Axis(format='.0%')),
                x=alt.X("day:N", title="Day",sort=None),
                tooltip=[
                        alt.Tooltip("PercentOfTotal:Q", title="PercentOfTotal",format='.2%'),
                    ],
            )
            fig = alt.layer(fig).configure_axis(
                labelFontSize=tick_size, titleFontSize=axis_title_size
            ).properties(title='Past 7 Days')

            st.altair_chart(fig, use_container_width=True)
            
            st.subheader('　│')

            st.markdown(' ')
            count_day = pd.read_csv('./past_7days/day_count_sui.csv')
            count_day.columns = ['day','count']
            cats = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            count_day = count_day.set_index('day').reindex(cats).reset_index()
            
            fig = alt.Chart(count_day).transform_joinaggregate(
                TotalTime='sum(count)',
            ).transform_calculate(
                PercentOfTotal="datum.count / datum.TotalTime"
            ).mark_bar(color="blue", size=35).encode(
                alt.Y('PercentOfTotal:Q', axis=alt.Axis(format='.0%')),
                x=alt.X("day:N", title="Day",sort=None),
                tooltip=[
                        alt.Tooltip("PercentOfTotal:Q", title="PercentOfTotal",format='.2%'),
                    ],
            )
            fig = alt.layer(fig).configure_axis(
                labelFontSize=tick_size, titleFontSize=axis_title_size
            ).properties(title='Past 7 Days')
            st.altair_chart(fig, use_container_width=True)

    elif menu == " Time  Frequency ":
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader('Depression Datasets')
            st.markdown(' ')
            count_hour = pd.read_csv('./before_pandemic/hour_count_dep.csv')
            count_hour.columns = ['hour','count']
            
            base = alt.Chart(count_hour).encode(x=alt.X("hour", title="Time",sort=None))
            fig = base.mark_line(color="red", size=3).encode(
                y=alt.Y("count", title="Count"),
                    tooltip=[
                        alt.Tooltip("hour", title="Time"),
                        alt.Tooltip("count", title="Count"),
                    ],
            )
            fig = alt.layer(fig).configure_axis(
                labelFontSize=tick_size, titleFontSize=axis_title_size
            ).properties(title='Before pandemic')

            st.altair_chart(fig, use_container_width=True)
            
            st.subheader('Suicide Datasets')

            st.markdown(' ')
            count_hour = pd.read_csv('./before_pandemic/hour_count_sui.csv')
            count_hour.columns = ['hour','count']
            
            base = alt.Chart(count_hour).encode(x=alt.X("hour", title="Time",sort=None))
            fig = base.mark_line(color="red", size=3).encode(
                y=alt.Y("count", title="Count"),
                    tooltip=[
                        alt.Tooltip("hour", title="Time"),
                        alt.Tooltip("count", title="Count"),
                    ],
            )
            fig = alt.layer(fig).configure_axis(
                labelFontSize=tick_size, titleFontSize=axis_title_size
            ).properties(title='Before pandemic')
            st.altair_chart(fig, use_container_width=True)

        with col2:

            st.subheader('　│')
            st.markdown(' ')
            count_hour = pd.read_csv('./after_pandemic/hour_count_dep.csv')
            count_hour.columns = ['hour','count']
            
            base = alt.Chart(count_hour).encode(x=alt.X("hour", title="Time",sort=None))
            fig = base.mark_line(color="green", size=3).encode(
                y=alt.Y("count", title="Count"),
                    tooltip=[
                        alt.Tooltip("hour", title="Time"),
                        alt.Tooltip("count", title="Count"),
                    ],
            )
            fig = alt.layer(fig).configure_axis(
                labelFontSize=tick_size, titleFontSize=axis_title_size
            ).properties(title='After pandemic')

            st.altair_chart(fig, use_container_width=True)
            
            st.subheader('　│')

            st.markdown(' ')
            count_hour = pd.read_csv('./after_pandemic/hour_count_sui.csv')
            count_hour.columns = ['hour','count']
            
            base = alt.Chart(count_hour).encode(x=alt.X("hour", title="Time",sort=None))
            fig = base.mark_line(color="green", size=3).encode(
                y=alt.Y("count", title="Count"),
                    tooltip=[
                        alt.Tooltip("hour", title="Time"),
                        alt.Tooltip("count", title="Count"),
                    ],
            )
            fig = alt.layer(fig).configure_axis(
                labelFontSize=tick_size, titleFontSize=axis_title_size
            ).properties(title='After pandemic')
            st.altair_chart(fig, use_container_width=True)
        
        with col3:
            st.subheader('　│')
            st.markdown(' ')
            count_hour = pd.read_csv('./past_7days/hour_count_dep.csv')
            count_hour.columns = ['hour','count']
            
            base = alt.Chart(count_hour).encode(x=alt.X("hour", title="Time",sort=None))
            fig = base.mark_line(color="blue", size=3).encode(
                y=alt.Y("count", title="Count"),
                    tooltip=[
                        alt.Tooltip("hour", title="Time"),
                        alt.Tooltip("count", title="Count"),
                    ],
            )
            fig = alt.layer(fig).configure_axis(
                labelFontSize=tick_size, titleFontSize=axis_title_size
            ).properties(title='Past 7 Days')

            st.altair_chart(fig, use_container_width=True)
            
            st.subheader('　│')

            st.markdown(' ')
            count_hour = pd.read_csv('./past_7days/hour_count_sui.csv')
            count_hour.columns = ['hour','count']
            
            base = alt.Chart(count_hour).encode(x=alt.X("hour", title="Time",sort=None))
            fig = base.mark_line(color="blue", size=3).encode(
                y=alt.Y("count", title="Count"),
                    tooltip=[
                        alt.Tooltip("hour", title="Time"),
                        alt.Tooltip("count", title="Count"),
                    ],
            )
            fig = alt.layer(fig).configure_axis(
                labelFontSize=tick_size, titleFontSize=axis_title_size
            ).properties(title='Past 7 Days')
            st.altair_chart(fig, use_container_width=True)

    elif menu == " Age  Frequency ":
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader('Depression Dataset')
            st.markdown(' ')
            count_age = pd.read_csv('./before_pandemic/age_count_dep.csv')
            count_age.columns = ['over_18','count']
            explode = (0, 0.1)
            fig, ax2 = plt.subplots()
            ax2.pie(count_age['count'], explode=explode, labels = count_age['over_18'],  autopct='%.2f%%', shadow=True, startangle=90)   
            ax2.set_xlabel('over_18')
            plt.title('Before pandemic')
            st.pyplot(fig)

            st.subheader('Suicide Dataset')
            st.markdown(' ')
            count_age = pd.read_csv('./before_pandemic/age_count_sui.csv')
            count_age.columns = ['over_18','count']
            fig, ax2 = plt.subplots()
            ax2.pie(count_age['count'],explode=explode, labels = count_age['over_18'],  autopct='%.2f%%', shadow=True, startangle=90)   
            ax2.set_xlabel('over_18')
            plt.title('Before pandemic')
            st.pyplot(fig)
        with col2:
            st.subheader('　│')
            st.markdown(' ')
            count_age = pd.read_csv('./after_pandemic/age_count_dep.csv')
            count_age.columns = ['over_18','count']
            explode = (0, 0.1)
            
            fig, ax2 = plt.subplots()
            colors = ['green' ,'red']
            ax2.pie(count_age['count'], explode=explode, colors=colors,labels = count_age['over_18'],  autopct='%.2f%%', shadow=True, startangle=90)   
            ax2.set_xlabel('over_18')
            plt.title('After pandemic')
            st.pyplot(fig)

            st.subheader('　│')
            st.markdown(' ')
            count_age = pd.read_csv('./after_pandemic/age_count_sui.csv')
            count_age.columns = ['over_18','count']
            fig, ax2 = plt.subplots()
            ax2.pie(count_age['count'],explode=explode,colors=colors, labels = count_age['over_18'],  autopct='%.2f%%', shadow=True, startangle=90)   
            ax2.set_xlabel('over_18')
            plt.title('After pandemic')
            st.pyplot(fig)
        with col3:
            st.subheader('　│')
            st.markdown(' ')
            colors = ['pink', 'yellow']

            count_age = pd.read_csv('./past_7days/age_count_dep.csv')
            count_age.columns = ['over_18','count']
            explode = (0, 0.1)
            fig, ax2 = plt.subplots()
            ax2.pie(count_age['count'], explode=explode, colors=colors, labels = count_age['over_18'],  autopct='%.2f%%', shadow=True, startangle=90)   
            ax2.set_xlabel('over_18')
            plt.title('Past 7 Days')
            st.pyplot(fig)

            st.subheader('　│')
            st.markdown(' ')
            count_age = pd.read_csv('./past_7days/age_count_sui.csv')
            count_age.columns = ['over_18','count']
            fig, ax2 = plt.subplots()
            ax2.pie(count_age['count'],explode=explode, colors=colors, labels = count_age['over_18'],  autopct='%.2f%%', shadow=True, startangle=90)   
            ax2.set_xlabel('over_18')
            plt.title('Past 7 Days')
            st.pyplot(fig)
        
    elif menu == " Word  Cloud ":
        col1, col2, col3 = st.columns(3)
        with col1:
            #wordcloud code
            st.subheader('Depression Dataset')
            st.markdown(' ')
            st.markdown("<h5 style='text-align: center; color: black;'>Before Pandemic</h5>", unsafe_allow_html=True)
            st.image('./before_pandemic/bp_depression.png')

            #wordcloud code
            st.subheader('Suicide Dataset')
            st.markdown(' ')
            st.markdown("<h5 style='text-align: center; color: black;'>Before Pandemic</h5>", unsafe_allow_html=True)
            st.image('./before_pandemic/bp_suicide.png')
        with col2:
            #wordcloud code
            st.subheader('　│')
            st.markdown(' ')
            st.markdown("<h5 style='text-align: center; color: black;'>After Pandemic</h5>", unsafe_allow_html=True)
            st.image('./after_pandemic/ap_depression.png')


            #wordcloud code
            st.subheader('　│')
            st.markdown(' ')
            st.markdown("<h5 style='text-align: center; color: black;'>After Pandemic</h5>", unsafe_allow_html=True)
            st.image('./after_pandemic/ap_suicide.png')
            

        with col3:
            #wordcloud code
            st.subheader('　│')
            st.text("")
            st.markdown("<h5 style='text-align: center; color: black;'>Past 7 Days</h5>", unsafe_allow_html=True)
            depression_data = pd.read_csv('./past_7days/depression.csv')
            depression_data = depression_data.dropna(axis=0)
            text = " ".join(content for content in depression_data.tibo)
            stopwords = set(STOPWORDS)
            wordcloud = WordCloud(stopwords=stopwords, background_color="white").generate(text)
            fig, ax = plt.subplots()
            plt.imshow(wordcloud, interpolation="bilinear")
            plt.axis("off")
            #plt.title('Past 7 Days')
            st.pyplot(fig)

            #wordcloud code
            st.subheader('　│')
            st.text("")
            st.markdown("<h5 style='text-align: center; color: black;'>Past 7 Days</h5>", unsafe_allow_html=True)
            suicide_data = pd.read_csv('./past_7days/suicide.csv')
            suicide_data = suicide_data.dropna(axis=0)
            text = " ".join(content for content in suicide_data.tibo)
            stopwords = set(STOPWORDS)
            wordcloud = WordCloud(stopwords=stopwords, background_color="white").generate(text)
            fig, ax = plt.subplots()
            plt.imshow(wordcloud, interpolation="bilinear")
            plt.axis("off")
            #plt.title('Past 7 Days')
            st.pyplot(fig) 

def set_posts():
    st.title('Top 15 Posts')
    depression_pro = predict_result()
    depression_pro1 = depression_pro[['title','full_link','time']]
    depression_pro1.index = range(1,len(depression_pro1)+1)
    def bg_colour_col(col):
        colour = '#ffff00'
        return ['background-color: %s' % colour if col.name == 'prob' or i == 4 else '' for i, x in col.iteritems()]
    def convert_click(link):
        return f'<a target="_blank" href="{link}">{link}</a>'

    
    #depression_pro1.style.format({'full_link': convert_click})
    depression_pro1.apply(bg_colour_col)
    depression_pro1['full_link'] = depression_pro1['full_link'].apply(convert_click)
    depression_pro1 = depression_pro1.to_html(escape=False).replace('<tr style="text-align: right;">', '<tr style="text-align: center;">')\
        #.replace('<table border="1" class="dataframe">', '<table border="1" class="dataframe" style="background-color:linear-gradient(red , yellow);">')
    pre_style = r'<style type="text/css"> table    { background-image: linear-gradient(#FFFAA0,white);} </style>' + '\n'
    pre_style += depression_pro1
    st.write(pre_style, unsafe_allow_html=True)
    #st.table(depression_pro1.style.apply(bg_colour_col))
    #st.dataframe(depression_pro1.style.apply(bg_colour_col), width=1024, height=768)
    #st.table(depression_pro1)
    #st.dataframe(depression_pro1.style.highlight_max(axis=0))