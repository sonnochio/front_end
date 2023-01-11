import json
import requests
import streamlit as st
from streamlit_lottie import st_lottie
import streamlit as st
from PIL import Image
import openai
from st_on_hover_tabs import on_hover_tabs
import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
from new_image import load_image,resize, convert_to_np
import os

openai.api_key = os.environ.get("OPENAI_API_KEY")




st.set_page_config(layout="wide")
st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)


with st.sidebar:
    tabs = on_hover_tabs(tabName=['Main', 'Predict','Team'],
                         iconName=['home', 'sync','groups'], default_choice=0)

if tabs =='Main':
    def load_lottieurl(url:str):
        r=requests.get(url)
        if r.status_code !=200:
            return None
        return r.json()

    url='https://assets9.lottiefiles.com/packages/lf20_qe6rfoqh.json'


    col1, col2 = st.columns([0.7,2])
    with col1:
        utube_logo=load_lottieurl(url)
        st_lottie(utube_logo,
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
                                                    left: 0px;
                                                    }}
                <style>
                """
        st.markdown(lottie_markdown, unsafe_allow_html=True)

    with col2:
        st.image('images/front_logo_white.png')
        logo_markdown = """
                <style>
                .css-1v0mbdj.etr89bj1 { border: none;
                float: left;
                width: 500px;
                height: 300px;
                margin: 100px 10px 390px 15px;

                                                    }
                <style>
                """
        st.markdown(logo_markdown, unsafe_allow_html=True)





        #   box-shadow:none;
        # #                                             float:left;
        #                                             width: 800px;
        #                                             height: 400px;
        # #                                             border: none;
        #                                             top: 100px;
        #                                             left: 0px;
    # st.write("# Youtube Optimizer")

    # st.write('Use the model to advise content creators on YouTube which thumbnails and titles they should use to maximise click-through rate.  ')


elif tabs == 'Predict':


    st.write("# Find the thumbnail and title to get the most views")

    st.write('Use this feature to find the best combination of thumbnails and titles for your next youtube video! Simply upload 3 thumbnails and think of possible titles for your video (the title generator will help you in case you can not think of a third title).')

    # st.write('---')

    st.write('    ')




    img_file_buffer = st.file_uploader('Upload the differnt thumbnails to choose from:', accept_multiple_files=True)
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
    st.write("     ")
    st.write("     ")
    st.write("     ")

    col1,col2, col3 = st.columns(3, gap="small")
    with col1:
        st.write('   ')
        st.markdown('## Insert your 1st title')
        title1 = st.text_input(' ')
    with col2:
        st.write('     ')
        st.markdown('## Insert your 2nd title')
        title2 = st.text_input('   ')
    with col3:
        with st.form("my_form"):
            # st.write("Inside the form")
            # slider_val = st.slider("Form slider")
            # checkbox_val = st.checkbox("Form checkbox")

            # # Every form must have a submit button.
            # submitted = st.form_submit_button("Submit")
            # if submitted:
            #     st.write("slider", slider_val, "checkbox", checkbox_val)

            st.markdown("## No idea? Get a title")
            # openai.api_key = st.secrets['openai_key']

            title3=st.text_input("Use GPT-3 to generate a title:")

            def generate_title_gtp3(text='kim kardashian'):
                response = openai.Completion.create(
                model="text-davinci-003",
                prompt=f"write a YouTube title about : {text}",
                temperature=0.7,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
                )
                return ((response["choices"])[0]["text"])

            if 'title3' not in st.session_state.keys():
                st.session_state["title3"] = title3
            get_title = st.form_submit_button('Get Title')
            if get_title:
                st.session_state["title3"] = generate_title_gtp3(title3)[1:-1]
            st.write((st.session_state["title3"]).replace('"',''))



    html = """
    <style>
        /* Disable overlay (fullscreen mode) buttons */
        .overlayBtn {
        display: none;
        }

        /* 2nd thumbnail */
        .css-1v0mbdj.etr89bj1 img{
            float: left;
            margin: 10px 15px -90px 15px;
        }



        }
    </style>
    """
    st.markdown(html, unsafe_allow_html=True)

    st.image("images/youtube.png", width=100)
    submitted = st.button('',key=3)


    button_markdown = f"""
    <style>
    .css-1cpxqw2.edgvbvh9:nth-child(1) {{ border: none;
                                        box-shadow:none;
                                        width: 120px;
                                        height: 70px;
                                        background-color: rgba(0,0,0,0);;
                                        border: none;
                                        }}
    <style>
    """
    st.markdown(button_markdown, unsafe_allow_html=True)

    titles = [title1,title2,st.session_state["title3"]]

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
            #response = requests.post('http://127.0.0.1:8000/test_predict', json=json.dumps(pred_dict))
            st.write(response)
            st.write(response.json)
            result = response.json()

            prediction = f"[{result['prediction'][1:-1].replace(']', '],')[:-1]}]"
            index = result['index']
            df = pd.DataFrame({'index':eval(index), 'prediction':eval(prediction)})
            df_A = df.merge(right = A, how = 'outer', on = 'index').sort_values("prediction", ascending = False)

        # st.table(df_A)
        comb_to_display = [0,1,2,-1]
        medals = ['images/medal.png',
                    'images/medal-2.png',
                    'images/medal-3.png',
                   'images/poop.png']

        for image in comb_to_display:
            with st.container():
                col1, col2,col3,col4,col5 = st.columns([0.5,4,2,2,0.5])
                with col1:
                    st.empty()
                with col2:
                    st.image(Image.open(img_file_buffer[df_A.iloc[image]['image_id']]),width = 400)
                    st.write('    ')
                    st.write('    ')
                    st.write('    ')
                    st.write('    ')
                    st.write('    ')
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
