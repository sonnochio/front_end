import streamlit as st
import altair as alt
import numpy as np
import pandas as pd
import pydeck as pdk
from PIL import Image
import requests
from io import BytesIO

# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
st.set_page_config(layout="wide", page_title="ABOUT US")

st.title('ABOUT US')

col1, col2,col3,col4,col5 = st.columns(5)

with col1:
    st.header("Jack")
    img_jack = Image.open('Jack.jpeg')
    st.image(img_jack)
    st.text('Jacky S')


with col2:
    st.header("Matt")
    img_matt = Image.open('Matt.png')
    st.image(img_matt)
    st.text("I dont know how to centre or format any of this - just figured out how to do this just before our meeting - didn't want to interrupt your workflow earlier")


with col3:
    st.header("Nicola")
    img_nicola = Image.open('Nicola.png')
    st.image(img_nicola)
    st.text('Nicki F')

with col4:
    st.header("Billy")
    img_billy = Image.open('Billy.png')
    st.image(img_billy)
    st.text('Billy W')


with col5:
    st.header('Sonny')
    img_sonny = Image.open('Sonny.jpeg')
    st.image(img_sonny)
    st.text('Sonny K')
