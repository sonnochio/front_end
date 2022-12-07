from streamlit_lottie import st_lottie
import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
from streamlit_option_menu import option_menu
from css import get_css

st.markdown(get_css(), unsafe_allow_html=True)
# insights_df = pd.read_csv('/Users/billy/code/youtube_optimizer/Insights_page/Data/final_processed_df.csv')
# data1=pd.read_csv('/Users/billy/code/youtube_optimizer/Insights_page/Data/barchart_df.csv')


# 1. horizontal menu
selected2 = option_menu(None, ["Hacks", "Emotions", "Word Cloud", "Faces"],
    icons=['gear', 'cloud-upload', "list-task", 'gear'],
    menu_icon="cast", default_index=0, orientation="horizontal")


# 2. sectional content
if selected2 == "Hacks":

    col1, col2= st.columns([5,5], gap="small")
    with col1:
        A = pd.DataFrame([['With','Capitals',0,0],
                    ['With','Capitals',3794,1],
                    ['Without','Capitals',0,0],
                    ['Without','Capitals',633,1],
                    ['With','Emojis',0,0],
                    ['With','Emojis',1402,1],
                    ['Without','Emojis',0,0],
                    ['Without','Emojis',633,1],
                    ['With','Numbers',0,0],
                    ['With','Numbers',1955,1],
                    ['Without','Numbers',0,0],
                    ['Without','Numbers',425,1]],columns = ['with','trick','views','play'])

        trick_options = ['Capitals', 'Emojis', 'Numbers']
        dummy_options = A['play'].unique().tolist()

        trick_bar = st.selectbox(
                ' ', options=['Capitals', 'Emojis', 'Numbers'])

        B = A[A['trick'].isin([trick_bar])]

        fig1 = px.bar(B, x='with', y='views', color='with', range_y=[0,4000], animation_frame="play",animation_group="with")
        fig1.update_xaxes(visible=False, showticklabels=False)
        fig1.update_layout(title=trick_bar, legend_title="")
        st.write(px.bar(B, x='with', y='views', color='with', range_y=[0,4000]))

        # st.write(fig1)

    with col2:
        if trick_bar == 'Capitals':
            with st.expander("See explanation"):
                st.write("""
                We found that simply having at least one word in all caps resulted in an average threefold increase in views.
            """)
            st.image("/Users/billy/code/youtube_optimizer/Insights_page/output-onlinepngtools.png", width=500)
        elif trick_bar == 'Emojis':
            with st.expander("See explanation"):
                st.write("""
                    We found that emojis were correlated with higher view count on average, when controlling for outliers.
                """)
                st.image("/Users/billy/code/youtube_optimizer/Insights_page/nerd-emoji-png-11536089702k3eqwusrcg.png", output_format='PNG', width=500)
        elif trick_bar == 'Numbers':
            with st.expander("See explanation"):
                st.write("""
                        We found having at least one number in a title significantly improves average view score. We understood this correltion to be in part explainable by the prevelance of high view count 'listicles'.
                """)
                st.image("/Users/billy/code/youtube_optimizer/Insights_page/blog-post-listicle-example-1.webp", output_format='PNG', width=500)

elif selected2 == "Emotions":
    st.write('Here be insights')

elif selected2 == "Word Cloud":
    st.write("Word Cloud here")

elif selected2 == "Faces":
    st.write("Faces Analysis here")
