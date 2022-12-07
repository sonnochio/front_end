import streamlit as st
import datetime
import requests
import pandas as pd
import numpy as np
import time
import streamlit as st
from PIL import Image
import requests
from dotenv import load_dotenv
import os
import json

# Set page tab display
st.set_page_config(
   page_title="Youtube optimizer",
   page_icon= '🖼️',
   layout="wide",
   initial_sidebar_state="expanded",
)

#load_dotenv()

tab1, tab2, tab3 = st.tabs(["image & title","1 image", "3 images"])

with tab2:
    # App title and description
    st.header('Viewcount Predictor 📸')

    ### Create a native Streamlit file upload input
    st.markdown("### How many clicks will your video get👇")
    img_file_buffer = st.file_uploader('Upload your thumbnail to get a prediction')

    url = 'https://taxifare.lewagon.ai/predict'

    if img_file_buffer is not None:

      col1, col2 = st.columns(2)

      with col1:
        ### Display the image user uploaded
        st.image(Image.open(img_file_buffer), caption="Here's the image you uploaded ☝️")

      with col2:
        with st.spinner("Wait for it..."):
          ### Get bytes from the file buffer
          #img_bytes = img_file_buffer.getvalue()

          ### Make request to  API (stream=True to stream response as bytes)
          res = requests.post(url)

          if res.status_code == 200:
            ### Display the image returned by the API
            st.image(res.content, caption="Image returned from API ☝️")
            st.write('Your video will be clicked ', res.json(),' times.')
          else:
            st.markdown("**Oops**, something went wrong 😓 Please try again.")
            print(res.status_code, res.content)

    st.markdown("---")

with tab2:
    st.header('Thumbnail Comparer 📸')
    st.markdown("### Unsure which thumbnail to use? Our model knows👇")



    im1, im2, im3 = st.columns(3, gap="small")

    with im1:
        img_file_buffer = st.file_uploader('Upload first thumbnail')
        if img_file_buffer is not None:
            st.image(Image.open(img_file_buffer), caption="Here's the image you uploaded ☝️")
            res1 = requests.post(url)
            st.write('A video with this thumbnail will be clicked ', res1.json(),' times.')

    with im2:
        img_file_buffer = st.file_uploader('Upload second thumbnail')
        if img_file_buffer is not None:
            st.image(Image.open(img_file_buffer), caption="Here's the image you uploaded ☝️")
            res2 = requests.post(url)
            st.write('A video with this thumbnail will be clicked ', res2.json(),' times.')

    with im3:
        img_file_buffer = st.file_uploader('Upload third thumbnail')
        if img_file_buffer is not None:
            st.image(Image.open(img_file_buffer), caption="Here's the image you uploaded ☝️")
            res3 = requests.post(url)
            st.write('A video with this thumbnail will be clicked ', res3.json(),' times.')

with tab1:
    # FINDING THE BEST COMBINATION OF TITEL AND THUMBNAIL

    st.header('Titles and Thumbnails Optimizer📸')
    st.markdown("### Let us find the best combination of Titles and Thumbnails for your Video👇")

    with st.form("my_form"):
        img_file_buffer = st.file_uploader('Upload the differnt thumbnails to choose from', accept_multiple_files=True)

        test_image = np.load('/Users/nicolafriedrich/Downloads/single_images_pred.npy')



        col1,col2, col3 = st.columns(3, gap="small")
        with col1:
            title1 = st.text_input('Insert your first title')
        with col2:
            title2 = st.text_input('Insert your second title')
        with col3:
            title3 = st.text_input('Insert your third title')

        submitted = st.form_submit_button("Submit")

        titles = [title1,title2,title3]

        if submitted:

            A = pd.DataFrame(columns = ["index","name","image_id","title"])

            image_id = 0
            images = []
            for image_buffer in img_file_buffer:
                image = Image.open(image_buffer)
                img_array = np.array(image)
                img_array = test_image[0]
                img_list = img_array.tolist()

                images.append(img_list)
                title_id = 0
                for title in titles:
                    name = f'{image}{title}'
                    add = pd.DataFrame({"index":[(title_id,image_id)],"name":[name],"image_id":[image_id],"title":[title]})
                    A = pd.concat([A,add],axis=0)#.sort_values("views", ascending = False)
                    title_id += 1
                image_id +=1


            pred_dict = {'image' : images,'text':titles }

            st.write(pred_dict)
            response = requests.post('http://127.0.0.1:8000/test_predict', json=json.dumps(pred_dict))
            #st.write(response)

            #pred_dict = response.text
            #st.write(response.text)


            result = response.json()
            st.write(result)

            prediction = f"[{result['prediction'][1:-1].replace(']', '],')[:-1]}]"
            st.write('prediction: ',prediction)

            index = result['index']
            st.write('index: ',index)

            df = pd.DataFrame({'index':eval(index), 'prediction':eval(prediction)})
            st.table(df)

            #st.table(A)

            df_A = df.merge(right = A, how = 'outer', on = 'index').sort_values("prediction", ascending = False)
            st.table(df_A)



            im1, im2, im3 = st.columns(3, gap="small")

            with im1:
                st.image(Image.open(img_file_buffer[df_A.iloc[-1]['image_id']]))
                st.write(df_A.iloc[-1]['title'])
                st.write("This will result in ",int(df_A.iloc[-1]['prediction'][0]),"clicks ❌")
                st.write("This is the worst performing combination")

            with im2:
                st.image(Image.open('/Users/nicolafriedrich/Downloads/Unknown-3'))
                worst_vc = int(df_A.iloc[-1]['prediction'][0])
                best_vc = int(df_A.iloc[0]['prediction'][0])
                st.write('You can improve this by ',round(((best_vc - worst_vc)/worst_vc)*100,2),' % 🥳')


            with im3:
                st.image(Image.open(img_file_buffer[df_A.iloc[0]['image_id']]))
                st.write(df_A.iloc[0]['title'])
                st.write("This will result in ",int(df_A.iloc[0]['prediction'][0]),"clicks ✅")
                st.write("This is the best performing combination")
