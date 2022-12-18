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
from streamlit_option_menu import option_menu
from streamlit_option_menu import option_menu
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from pyplutchik import plutchik
import matplotlib.pyplot as plt
from skimage import io
from new_image import load_image,resize, convert_to_np




st.set_page_config(layout="wide")
st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)


with st.sidebar:
    tabs = on_hover_tabs(tabName=['Main', 'Predict', 'Analysis','Future','Team'],
                         iconName=['home', 'sync', 'hub','rocket_launch','groups'], default_choice=0)

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
        st.image('images/fron_logo.png')
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
            openai.api_key = st.secrets['openai_key']

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

            response = requests.post('https://youtube1-nct5cxzhzq-ew.a.run.app/test_predict', json=json.dumps(pred_dict))
            #response = requests.post('http://127.0.0.1:8000/test_predict', json=json.dumps(pred_dict))

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





elif tabs == 'Analysis':
    emotions = {'joy': 0.6,
            'trust': 0.4,
            'fear': 0.2,
            'surprise': 0.7,
            'sadness': 0.4,
            'disgust': 0.1,
            'anger': 0.4,
            'anticipation': 0.35}

    emotions2 = {'joy': 0.5,
                'trust': 0.4,
                'fear': 0.3,
                'surprise': 0.7,
                'sadness': 0.4,
                'disgust': 0.1,
                'anger': 0.4,
                'anticipation': 0.3}


    def make_pie(df):

        data = [(df['anger'] != 0).sum(), (df['anticip'] != 0).sum(),
            (df['trust'] != 0).sum(), (df['surprise'] != 0).sum(),
            (df['sadness'] != 0).sum(), (df['disgust'] != 0).sum(),
            (df['joy'] != 0).sum()]

        keys = ['Anger', 'Anticipation', 'Trust', 'Surprise', 'Sadness', 'Disgust', 'Joy']

        fig = px.pie(df, values=data, names=keys, title='Sentiment Pie Chart')

        return fig

    def make_vader_pie(df):

        data = [(df['neg'] != 0).sum(), (df['neu'] != 0).sum(),
                (df['pos'] != 0).sum()]

        keys = ['neg', 'neu', 'pos']

        fig = px.pie(df, values=data, names=keys, title='Sentiment Pie Chart', hole=.3)

        return fig


    vader_top10 = pd.read_csv('data/vader_top10.csv')

    vader_bottom10 = pd.read_csv('data/vader_bottom10.csv')


    # st.markdown(get_css(), unsafe_allow_html=True)

    # 2. horizontal menu
    selected2 = option_menu(None, ["Click Triggers", "Word Cloud", "Sentiment Analysis"],
        icons=['hand-index', "emoji-smile", "cloud"],
        menu_icon="cast", default_index=0, orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "orange", "font-size": "20px"},
            "nav-link": {"font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "red"},
        }
    )

    if selected2 == "Click Triggers":
        with st.container():
            col1, col2= st.columns([1,1])
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


                base = (((1.77*29)+(0.668*3))/32)
                C = pd.DataFrame([['1',0,0],
                                ['1',4.4/base,1],
                                ['2',0,0],
                                ['2',4.02/base,1],
                                ['3+',0,0],
                                ['3+',base/base,1]],columns = ['Number','Proportional views','play'])

                trick_bar = st.selectbox("",options=['Capitals', 'Emojis', 'Numbers', 'Faces'])

                if trick_bar == 'Faces':

                    fig1 = px.bar(C, x='Number', y='Proportional views', color='Number', range_y=[0,4], animation_frame="play",animation_group="Number")
                    fig1.update_xaxes(visible=False, showticklabels=False)
                    fig1.update_layout(title=trick_bar, legend_title="")

                else:
                    B = A[A['trick'].isin([trick_bar])]
                    fig1 = px.bar(B, x='with', y='views', color='with', range_y=[0,4000], animation_frame="play",animation_group="with")
                    fig1.update_xaxes(visible=False, showticklabels=False)
                    fig1.update_layout(title=trick_bar, legend_title="")
                # st.write(px.bar(B, x='with', y='views', color='with', range_y=[0,4000]))

                # trick_bar = st.selectbox(
                #         ' ', options=['Capitals', 'Emojis', 'Numbers'])

                st.write(fig1)

            with col2:
                st.write("")
                st.write("")
                if trick_bar == 'Capitals':
                    with st.expander("See explanation"):
                        st.write("""
                        We found that simply having at least one word in all caps resulted in an average threefold increase in views.
                    """)
                        st.image("images/mouth.png", width=500)
                elif trick_bar == 'Emojis':
                    with st.expander("See explanation"):
                        st.write("""
                            We found that emojis were correlated with higher view count on average, when controlling for outliers.
                        """)
                        st.image("images/emoji.jpeg", width=500)
                elif trick_bar == 'Numbers':
                    with st.expander("See explanation"):
                        st.write("""
                                We found having at least one number in a title significantly improves average view score. We understood this correltion to be in part explainable by the prevelance of 'listicles' with high view counts.
                        """)
                        st.image("images/blog.webp", output_format='PNG', width=500)
                elif trick_bar == 'Faces':
                    with st.expander("See explanation"):
                        st.write("""
                                We ran the CV2 Face Detection Model on the dataset, and found having more than two faces was detrimental to view count.
                        """)
                        st.image("images/marylin.jpeg", output_format='PNG', width=500)


    elif selected2 == "Word Cloud":
        col1, col2 = st.columns([2,2], gap='medium')
        with col1:
            st.title('Best performing 10% of videos')
            st.image('images/topstop.png')
            with st.expander("See explanation"):
                        st.write("""
                        After removing common stopwords, and hashtags for categories like #shorts, we found that the most common word in the most successful 10% of videos was 'vs'. This indicates that including 'vs' in your title may also act as a click trigger.
                    """)


        with col2:
            st.title('Worst performing 10% of videos')
            st.image('images/bottomstop.png')
            with st.expander("See explanation"):
                        st.write("""
                        After removing stopwords and hashtags, we found the most common words in the least well performing 10% of videos to be as above. Youtubers don't like love.. :(
                    """)

    elif selected2 == "Sentiment Analysis":
        col1, col2 = st.columns([2,2], gap='small')
        with col1:
            st.subheader("Sentiment distribution of top 10% by viewcount")
            fig = make_vader_pie(vader_top10)
            fig.update_layout(title='')
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig)


            # fig1=make_pie(top10)
            # fig1.update_layout(title='Emotion distribution of top 10% of videos by viewcount')
            # st.plotly_chart(fig1)
            st.write("")
            st.write("")
            st.subheader("Best Performing 10% emotion detection")
            fig, ax = plt.subplots(1, figsize=(7,7))
            plutchik(emotions, ax, fontweight = 'light',
                fontsize = 10)
            st.pyplot(fig)

        with col2:
            st.subheader("Sentiment distribution of bottom 10% by viewcount")
            fig3 = make_vader_pie(vader_bottom10)
            fig3.update_layout(title='')
            fig3.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig3)


            # fig2=make_pie(bottom10)
            # fig2.update_layout(title='Emotion distribution of bottom 10% of videos by viewcount')
            # st.plotly_chart(fig2)
            st.write("")
            st.write("")
            st.subheader("Worst performing 10% emotion detection")
            fig, ax = plt.subplots(1, figsize=(7,7))
            plutchik(emotions2, ax, fontweight = 'light',
                fontsize = 10)
            st.pyplot(fig)

elif tabs == 'Future':
    st.markdown("# Not feeling creative? Here's a thumbnail for you !")

    def image_generate_dalle(text):
        openai.api_key =st.secrets['dalle']
        response = openai.Image.create(
        prompt= f'youtube thumbnail about {text}',
        n=1,
        size="1024x1024"
        )
        image_url = response['data'][0]['url']

        return image_url

    key_words=st.text_input("Use DALL-E to generate a thumbnail:")

    image_url=image_generate_dalle(key_words)

    a=io.imread(image_url)
    st.image(a)

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
