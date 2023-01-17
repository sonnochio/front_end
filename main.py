import json
import requests
import streamlit as st
from streamlit_lottie import st_lottie
import streamlit as st
from PIL import Image
import openai
from st_on_hover_tabs import on_hover_tabs
import streamlit as st
import numpy as np
import pandas as pd
from new_image import load_image,resize, convert_to_np
import os

openai.api_key = os.environ.get("OPENAI_API_KEY")
# openai.api_key = st.secrets['openai_key']


st.set_page_config(layout="wide")
st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)

def generate_title_gtp3(title1,title2):
            response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Write a successful YouTube title from these two titles: \n\n '{title1}' and '{title2}' .",
            temperature=0.7,
            max_tokens=256,
            frequency_penalty=0,
            presence_penalty=0
            )
            return ((response["choices"])[0]["text"])


with st.sidebar:
    tabs = on_hover_tabs(tabName=['Main', 'Optimize','Team'],
                         iconName=['home', 'bolt','groups'], default_choice=0)

if tabs =='Main':
    def load_lottieurl(url:str):
        r=requests.get(url)
        if r.status_code !=200:
            return None
        return r.json()

    url='https://assets9.lottiefiles.com/packages/lf20_qe6rfoqh.json'


    col0, col1, col2, col3 = st.columns([0.1,1.4,0.1,2.95])
    with col1:
        youtube_logo=load_lottieurl(url)
        st_lottie(youtube_logo,
                speed=0.3,
                key='title',
                height=500,
                width=300)

        lottie_markdown = f"""
                <style>
                .svg {{ border: none;
                                                    box-shadow:none;
                                                    float:left;
                                                    width: 200px;
                                                    height: 30px;
                                                    border: none;
                                                    top: 0px;
                                                    left: 1000px;
                                                    }}
                <style>
                """
        st.markdown(lottie_markdown, unsafe_allow_html=True)

    with col3:
        st.image('images/front_logo_black.png')
        logo_markdown = """
                <style>
                .css-1v0mbdj.etr89bj1 { border: none;
                float: left;
                width: 540px;
                height: 300px;
                margin: 100px 10px 390px 15px;

                                                    }
                <style>
                """
        st.markdown(logo_markdown, unsafe_allow_html=True)

elif tabs == 'Optimize':


    st.write("# Optimize Title and Thumbnail Combination")

    st.write('''###### Use this feature to find the best combination of thumbnail and title for your next youtube video!''')
    st.write('''The model will combine 3 images and 3 titles to predict the best combination.''')

    # st.write('---')

    st.write('    ')



    st.markdown('## Upload 3 Images')
    img_file_buffer = st.file_uploader('Upload exactly 3 different thumbnails to combine:', accept_multiple_files=True)
    # st.write(len(img_file_buffer))

    if len(img_file_buffer) == 3:
        col1,col2, col3 = st.columns(3, gap="small")
        with col1:
            st.image(Image.open(img_file_buffer[0]),width = 400)

        with col2:
            st.image(Image.open(img_file_buffer[1]),width = 400)

        with col3:
            st.image(Image.open(img_file_buffer[2]),width = 400)

    st.write("     ")
    st.write("     ")
    st.write("     ")

    col1,col2, col3 = st.columns([1.5,1.5,2])
    with col1:
        st.write('   ')
        st.markdown('## Input Title 1')
        title1 = st.text_input(' ')
        st.write(' ')

        st.write("""The first prediction will take around 1 minute. Following predictions will take around 10 seconds.""")

    with col2:
        st.write('     ')
        st.markdown('## Input Title 2')
        title2 = st.text_input('   ')
    with col3:
        st.write('     ')
        st.write('     ')
        # st.markdown('## Title Idea 3')

        # get_title = st.button("Button Text", button_style='font-size: 40px;')
        get_title = st.button(' Use Chat-GPT to generate Title Idea 3')

        if get_title:
            st.session_state["key"] = generate_title_gtp3(title1,title2)[1:-1]
        if "key" in st.session_state.keys():
            title3=st.text_input("", value = st.session_state["key"].replace('"',''))
        else:
            title3=st.text_input("", value = '')


    submitted = st.button('GENERATE RESULTS',key=3)

    titles = [title1,title2,title3]

    if submitted:
        with st.spinner('Wait for it...'):
            # time.sleep(10)
            # st.success('Wait a bit longer!')

            A = pd.DataFrame(columns = ["index","name","image_id","title"])

            image_id = 0
            images = []
            for image_buffer in img_file_buffer:
                image = Image.open(image_buffer)
                image=resize(image)
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

            response = requests.post('https://youtube2-nct5cxzhzq-ew.a.run.app/test_predict', json=json.dumps(pred_dict))
            result = response.json()

            prediction = f"[{result['prediction'][1:-1].replace(']', '],')[:-1]}]"
            index = result['index']
            df = pd.DataFrame({'index':eval(index), 'prediction':eval(prediction)})
            df_A = df.merge(right = A, how = 'outer', on = 'index').sort_values("prediction", ascending = False)

        st.write('##')
        st.write('##')
        comb_to_display = [0,1,2,-1]
        medals = ['images/medal_gold.png',
                    'images/medal_silver.png',
                    'images/medal_bronze.png',
                   'images/poop.png']

        for image in comb_to_display:
            with st.container():
                col1, col2,col3,col4,col5,col6, col7 = st.columns([0.5,1.5,0.5,2.5,0.5,1.5,0.5])
                with col1:
                    st.empty()
                with col5:
                    st.empty()
                with col4:
                    # st.m
                    # st.subheader(df_A.iloc[image]['title'])
                    st.write('    ')
                    st.image(Image.open(img_file_buffer[df_A.iloc[image]['image_id']]),width = 400)
                    st.markdown(f"<h3 style='text-align: left;'>{df_A.iloc[image]['title']}</h1>", unsafe_allow_html=True)

                    # st.write('    ')
                with col6:
                    worst_vc = int(df_A.iloc[-1]['prediction'][0])
                    best_vc = int(df_A.iloc[image]['prediction'][0])
                    improvement = f'{round(((best_vc - worst_vc)/worst_vc)*100,2)}%'
                    # st.write('    ')
                    st.write('    ')
                    st.write('    ')
                    st.write('    ')
                    st.write('    ')
                    st.markdown(
                        """
                        <style>
                        [data-testid="stMetricValue"] {
                            font-size: 50px;
                        }
                        </style>
                        """,unsafe_allow_html=True,)

                    # st.metric(label="Metric", value=1000, delta=100)
                    st.metric('Expected Views', int(df_A.iloc[image]['prediction'][0]), delta=improvement, delta_color="normal", help=None)
                with col2:
                    st.image(Image.open(medals[image]),width = 240)
                with col7:
                    st.empty()
                st.empty()
                st.markdown("---")

elif tabs == 'Team':
    st.title('ABOUT US')

    col1, col2,col3,col4,col5 = st.columns(5)

    with col1:
        st.header("Jack")
        img_jack = Image.open('images/Jack.jpeg')
        st.image(img_jack)
        st.text('Jacky S')


    with col2:
        st.header("Matt")
        img_matt = Image.open('images/Matt.png')
        st.image(img_matt)
        st.text("Matt C")


    with col3:
        st.header("Nicola")
        img_nicola = Image.open('images/Nicola.png')
        st.image(img_nicola)
        st.text('Nicki F')

    with col4:
        st.header("Billy")
        img_billy = Image.open('images/Billy.png')
        st.image(img_billy)
        st.text('Billy W')


    with col5:
        st.header('Sonny')
        img_sonny = Image.open('images/Sonny.jpeg')
        st.image(img_sonny)
        st.text('Sonny K')
