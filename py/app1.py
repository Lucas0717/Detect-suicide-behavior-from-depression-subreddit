import streamlit as st
from app2 import *

st.set_page_config(page_title='Reddit',
                   page_icon='https://media.wired.com/photos/5954a1b05578bd7594c46869/master/w_2560%2Cc_limit/reddit-alien-red-st.jpg',
                   layout="wide")

st.sidebar.image('https://play-lh.googleusercontent.com/MDRjKWEIHO9cGiWt-tlvOGpAP3x14_89jwAT-nQTS6Fra-gxfakizwJ3NHBTClNGYK4', width=300)
st.sidebar.header('Navigation')
#st.markdowns('<h1 style="text-align:center;color:white;font-weight:bolder;font-size:100px;">Reddit<br>OF<br>THRONES</h1>',unsafe_allow_html=True)
#st.sidebar.markdown('Detect suicide behavior in depression subreddit| Past 7 days')


menu = st.sidebar.radio(
    "",
    ("Intro",
    "Top Posts",
     "Data Analysis"),
)

# Pone el radio-button en horizontal. Afecta a todos los radio button de una página.
# Por eso está puesto en este que es general a todo

st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

st.sidebar.markdown('---')
st.sidebar.write('Team JHP')
st.sidebar.write('Lishi Ji | Gangyu Pan | Jiabao He')
if menu == 'Intro':
    set_intro()
if menu == 'Top Posts':
    set_posts()
elif menu == 'Data Analysis':
    set_data()