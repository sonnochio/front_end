import streamlit as st
import requests
import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image
import requests
import json
import time
import openai

# Set page tab display
st.set_page_config(
   page_title="Youtube optimizer",
   page_icon= '🖼️',
   layout="wide",
   initial_sidebar_state="expanded",
)

st.header('Titles and Thumbnails Optimizer📸')
st.markdown("### Let us find the best combination of Titles and Thumbnails for your Video👇")

#with st.form("my_form"):
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
        title3 = "coffee"
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
    medals = ['/Users/nicolafriedrich/Downloads/medal.png',
                  '/Users/nicolafriedrich/Downloads/medal-2.png',
                  '/Users/nicolafriedrich/Downloads/medal-3.png',
                  '/Users/nicolafriedrich/Downloads/poop.png']

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
