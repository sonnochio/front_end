import openai
from skimage import io
import streamlit as st

st.markdown("# Not feeling creative? Here's a thumbnail for you lazy fuck")

def image_generate_dalle(text):
    openai.api_key =st.secrets['dalle']
    response = openai.Image.create(
    prompt= f'youtube thumbnail about {text}',
    n=1,
    size="1024x1024"
    )
    image_url = response['data'][0]['url']

    return image_url

key_words=st.text_input("example: coffee, le wagon, jobs")

image_url=image_generate_dalle(key_words)

a=io.imread(image_url)
st.image(a)
