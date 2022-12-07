import streamlit as st
import pandas as pd

html = """
  <style>
    /* Disable overlay (fullscreen mode) buttons */
    .overlayBtn {
      display: none;
    }

    /* 2nd thumbnail */
    .element-container:nth-child(4) {
      top: 266px;
      left: 500px;
    }

    /* 1st button */
    .element-container:nth-child(3) {
      left: 100px;
      top: -150px;
    }

    }
  </style>
"""
st.markdown(html, unsafe_allow_html=True)

# st.image("youtube-1495277_1280.png", width=320)

st.button("button", key=1)

button_markdown = f"""
<style>
div.stButton > button:first-child {{ border: none;
                                    box-shadow:none;
                                    background: url("youtube-1495277_1280.png");
                                    width: 300px;
                                    height: 300px;
                                    background-size: cover;

                                    }}
<style>
"""
st.markdown(button_markdown, unsafe_allow_html=True)
