import streamlit as st
import openai


st.markdown("# Got no idea? Generate a title")

openai.api_key = st.secrets['openai_key']
#  "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"


key_words=st.text_input("example: coffee, le wagon, jobs")

def generate_title_gtp3(text):

    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=f"write a YouTube title about {text}",
      temperature=0.7,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )

    return response

if len(key_words)>0:
    a=generate_title_gtp3(key_words)
    st.write(a)
    st.write(a["choices"][0]["text"])


# import time

#     'Starting a long computation...'

#     # Add a placeholder
#     latest_iteration = st.empty()
#     bar = st.progress(0)

#     for i in range(100):
#         # Update the progress bar with each iteration.
#         latest_iteration.text(f'Iteration {i+1}')
#         bar.progress(i + 1)
#         time.sleep(0.1)

#     '...and now we\'re done!'
