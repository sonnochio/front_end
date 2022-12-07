import json
import requests
import streamlit as st
from streamlit_lottie import st_lottie
import streamlit as st
from PIL import Image
import time
import openai
from st_on_hover_tabs import on_hover_tabs
import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
from streamlit_option_menu import option_menu
from css import get_css








st.set_page_config(layout="wide")
st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)


with st.sidebar:
    tabs = on_hover_tabs(tabName=['Main', 'Predict', 'Analysis'],
                         iconName=['home', 'sync', 'hub'], default_choice=0)

if tabs =='Main':
    def load_lottieurl(url:str):
        r=requests.get(url)
        if r.status_code !=200:
            return None
        return r.json()

    url='https://assets9.lottiefiles.com/packages/lf20_qe6rfoqh.json'


    utube_logo=load_lottieurl(url)


    st_lottie(utube_logo,
            speed=0.3,
            key='title',
            height=300,
            width=200)
    st.write("# Youtube Optimizer")

    st.write('Use the model to advise content creators on YouTube which thumbnails and titles they should use to maximise click-through rate.  ')





elif tabs == 'Predict':


    # Set page tab display
    # st.set_page_config(
    # page_title="Youtube optimizer",
    # page_icon= '🖼️',
    # layout="wide",
    # initial_sidebar_state="expanded",
    # )

    # st.header('Titles and Thumbnails Optimizer📸')
    # st.markdown("### Let us find the best combination of Titles and Thumbnails for your Video👇")

    #with st.form("my_form"):
    # st.write('#')
    img_file_buffer = st.file_uploader('Upload the differnt thumbnails to choose from', accept_multiple_files=True)




    col1,col2, col3 = st.columns(3, gap="small")
    with col1:
        st.markdown('## Insert your 1st title')
        title1 = st.text_input('Insert your 1st title')
    with col2:
        st.markdown('## Insert your 2nd title')
        title2 = st.text_input('Insert your 2nd title')
    with col3:
        st.markdown("## No idea? Get a title")
        openai.api_key = st.secrets['openai_key']
        #"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"
        title3=st.text_input("example: coffee, le wagon, jobs")

        def generate_title_gtp3(text='kim kardashian'):
            response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"write a YouTube title about {text}",
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
            )
            return ((response["choices"])[0]["text"])

        get_title = st.button('Get Title')
        if get_title:
            st.write(generate_title_gtp3(title3))
            title3 = generate_title_gtp3(title3)[1:-1]
            if "title3" not in st.session_state.keys():
                st.session_state["title3"] = title3
        else:
            # title3 = "coffee"
            st.session_state["title3"] = title3


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



        }
    </style>
    """
    st.markdown(html, unsafe_allow_html=True)

    # st.image("youtube-1495277_1280.png", width=320)
    submitted = st.button('Submit')

    # st.button("button", key=1)

    button_markdown = f"""
    <style>
    .row-widget.stButton{{ border: none;
                                        box-shadow:none;
                                        width: 150px;
                                        height: 100px;
                                        background-size: cover;

                                        }}
    <style>
    """
    st.markdown(button_markdown, unsafe_allow_html=True)

    titles = [title1,title2,st.session_state["title3"]]

    if submitted:

        with st.spinner('Wait for it...'):
            time.sleep(5)
            st.success('Done!')

        A = pd.DataFrame(columns = ["index","name","image_id","title"])

        image_id = 0
        images = []
        for image_buffer in img_file_buffer:
            image = Image.open(image_buffer)
            img_array = np.array(image)
            img_list = img_array.tolist()
            images.append(img_list)
            title_id = 0
            for title in titles:
                name = f'{image}{title}'
                add = pd.DataFrame({"index":[(title_id,image_id)],"name":[name],"image_id":[image_id],"title":[title]})
                A = pd.concat([A,add],axis=0)
                title_id += 1
            image_id +=1

        pred_dict = {'image' : images,'text':titles }

        response = requests.post('https://youtube1-nct5cxzhzq-ew.a.run.app/test_predict', json=json.dumps(pred_dict))
        #response = requests.post('http://127.0.0.1:8000/test_predict', json=json.dumps(pred_dict))

        result = response.json()
        prediction = f"[{result['prediction'][1:-1].replace(']', '],')[:-1]}]"
        index = result['index']
        df = pd.DataFrame({'index':eval(index), 'prediction':eval(prediction)})
        df_A = df.merge(right = A, how = 'outer', on = 'index').sort_values("prediction", ascending = False)

        st.table(df_A)
        comb_to_display = [0,1,2,-1]
        medals = ['medal.png',
                    'medal-2.png',
                    'medal-3.png',
                   'poop.png']

        for image in comb_to_display:
            with st.container():
                col1, col2,col3,col4,col5 = st.columns([0.5,4,2,2,0.5])
                with col1:
                    st.empty()
                with col2:
                    st.image(Image.open(img_file_buffer[df_A.iloc[image]['image_id']]),width = 400)
                    st.subheader(df_A.iloc[image]['title'])
                with col3:
                    worst_vc = int(df_A.iloc[-1]['prediction'][0])
                    best_vc = int(df_A.iloc[image]['prediction'][0])
                    improvement = f'{round(((best_vc - worst_vc)/worst_vc)*100,2)}%'
                    st.metric('Expected Views', int(df_A.iloc[image]['prediction'][0]), delta=improvement, delta_color="normal", help=None)
                with col4:
                    st.image(Image.open(medals[image]),width = 120)
                with col5:
                    st.empty()
                st.empty()
                st.markdown("---")














































elif tabs == 'Analysis':
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






















# with st.sidebar:
#         tabs = on_hover_tabs(tabName=['Dashboard', 'Money', 'Economy'],
#                              iconName=['dashboard', 'money', 'economy'],
#                              styles = {'navtab': {'background-color':'#111',
#                                                   'color': '#818181',
#                                                   'font-size': '18px',
#                                                   'transition': '.3s',
#                                                   'white-space': 'nowrap',
#                                                   'text-transform': 'uppercase'},
#                                        'tabOptionsStyle': {':hover :hover': {'color': 'red',
#                                                                       'cursor': 'pointer'}},
#                                        'iconStyle':{'position':'fixed',
#                                                     'left':'7.5px',
#                                                     'text-align': 'left'},
#                                        'tabStyle' : {'list-style-type': 'none',
#                                                      'margin-bottom': '30px',
#                                                      'padding-left': '30px'}},
#                              key="1")


# if tabs =='Dashboard':
#     st.title("Navigation Bar")
#     st.write('Name of option is {}'.format(tabs))

# elif tabs == 'Money':
#     st.title("Paper")
#     st.write('Name of option is {}'.format(tabs))

# elif tabs == 'Economy':
#     st.title("Tom")
#     st.write('Name of option is {}'.format(tabs))


# import utils as utlg
# from views import home,about,analysis,options,configuration



# def navigation():
#     route = utl.get_current_route()
#     if route == "home":
#         home.load_view()
#     elif route == "about":
#         about.load_view()
#     elif route == "analysis":
#         analysis.load_view()
#     elif route == "options":
#         options.load_view()
#     elif route == "configuration":
#         configuration.load_view()
#     elif route == None:
#         home.load_view()

# navigation()


# st.set_page_config(layout="wide", page_title='Youtube Optmizer')
# st.set_option('deprecation.showPyplotGlobalUse', False)
# utl.inject_custom_css()
# utl.navbar_component()

# def load_lottiefile(filepath:str):
#     with open(filepath,"r") as f:
#         return json.load(f)
