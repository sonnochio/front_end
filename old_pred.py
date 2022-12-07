import streamlit as st
import requests
import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image
import requests
#from dotenv import load_dotenv
import json
import time
import pandas as pd



# Set page tab display
st.set_page_config(
   page_title="Youtube optimizer",
   page_icon= '🖼️',
   layout="wide",
   initial_sidebar_state="expanded",
)

st.header('Titles and Thumbnails Optimizer📸')
st.markdown("### Let us find the best combination of Titles and Thumbnails for your Video👇")

with st.form("my_form"):
    img_file_buffer = st.file_uploader('Upload the differnt thumbnails to choose from', accept_multiple_files=True)

    col1,col2, col3 = st.columns(3, gap="small")
    with col1:
        title1 = st.text_input('Insert your first title')
    with col2:
        title2 = st.text_input('Insert your second title')
    with col3:
        title3 = st.text_input('Insert your third title')




    html = """
    <style>
        /* Disable overlay (fullscreen mode) buttons */
        .overlayBtn {
        display: none;
        }

        /* 2nd thumbnail */
        .element-container:nth-child(4) {
        top: 79px;
        left: 0px;
        }

        /* 1st button */
        .element-container:nth-child(3) {
        left: 100px;
        top: 0px;
        }

        }
    </style>
    """
    st.markdown(html, unsafe_allow_html=True)

    st.image("youtube-1495277_1280.png", width=140)


    submitted=st.form_submit_button("")
    # with col

    button_markdown = f"""
    <style>
    .css-1cpxqw2.edgvbvh5 {{ border: none;
                            box-shadow:none;
                            background-color:rgba(0,0,0,0);
                            width: 150px;
                            height: 50px;
                            }}



    <style>
    """


    st.markdown(button_markdown, unsafe_allow_html=True)





    titles = [title1,title2,title3]

    if submitted:

        my_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.8)
            my_bar.progress(percent_complete + 1)

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

        response = requests.post('http://127.0.0.1:8000/test_predict', json=json.dumps(pred_dict))
        result = response.json()

        prediction = f"[{result['prediction'][1:-1].replace(']', '],')[:-1]}]"

        index = result['index']

        df = pd.DataFrame({'index':eval(index), 'prediction':eval(prediction)})

        df_A = df.merge(right = A, how = 'outer', on = 'index').sort_values("prediction", ascending = False)


        comb_to_display = [0,1,2,-1]
        medals = ['/Users/nicolafriedrich/Downloads/medal',
                  '/Users/nicolafriedrich/Downloads/medal-2',
                  '/Users/nicolafriedrich/Downloads/medal-3',
                  '/Users/nicolafriedrich/Downloads/poop']

        for image in comb_to_display:
            with st.container():
                col1, col2,col3,col4 = st.columns([1,3,2,2])
                with col1:
                    st.empty()
                with col2:
                    st.image(Image.open(img_file_buffer[df_A.iloc[image]['image_id']]),caption =df_A.iloc[image]['title'] )
                with col3:
                    worst_vc = int(df_A.iloc[-1]['prediction'][0])
                    best_vc = int(df_A.iloc[image]['prediction'][0])
                    improvement = f'{round(((best_vc - worst_vc)/worst_vc)*100,2)}%'
                    st.metric('Expected Views', int(df_A.iloc[image]['prediction'][0]), delta=improvement, delta_color="normal", help=None)
                with col4:
                    st.image(Image.open(medals[image]))
