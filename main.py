# I am using streamlit libraries

import os

import streamlit as st

from PIL import Image
from streamlit_option_menu import option_menu

from gemini_utility import (load_model, load_vision_model,embedding_response,gemini_response)

# get the working directory
Working_directory = os.path.dirname(os.path.abspath(__file__))

# setting up the page config
st.set_page_config(
    page_title="Rocker AI",
    page_icon="🐺",
    layout="centered"
)

with st.sidebar:

    selected = option_menu("Rocker AI",
                           ["ChatBot",
                            "Image Captioning",
                            "Embed text",
                            "Ask Me Anything"],
                           menu_icon='robot', icons=['chat-square-quote-fill','file-earmark-image',
                                                     'body-text','patch-question-fill'],
                           default_index=0)
# function to translate role between gemini-pro and streamlit terminologies


def translate_role_for_streamlit(user_role):
    if user_role == 'model':
        return "assistant"
    else:
        return user_role


if selected == "ChatBot":

    model = load_model()

    # maintaining the state to remember previous conversation(chat session)
    # initialize_chat_session in streamlit if not present
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])
    # streamlit page title
    st.title("🤖ChatBot🦾")
    # display the chat history
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    # input field for user's message
    user_prompt = st.chat_input("Ask Rocker AI.....")

    if user_prompt:
        st.chat_message("user").markdown(user_prompt)

        gemini_response = st.session_state.chat_session.send_message(user_prompt)

        # Display gemini-pro response
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)



# Image Captioning page
if selected == "Image Captioning":
    # streamlit page title
    st.title("Snap📸Caption")

    upload_image = st.file_uploader("Upload an Image......", type=["jpg", "jpeg", "png"])

    if st.button("Generate Caption"):

        image = Image.open(upload_image)

        col1, col2 = st.columns(2)

        with col1:
            resize_image = image.resize((900, 600))
            st.image(resize_image)

        default_prompt = "write a short caption for this image"

        # getting the response from gemini pro vision
        caption = load_vision_model(default_prompt, image)

        with col2:
            st.info(caption)


# text embedding page
if selected == "Embed text":
    st.title("Get 🔢 Embeded Text")

    # input text box
    input_text = st.text_area(label=" ", placeholder="Enter the Text...........")

    if st.button('Get Embeddings'):
        response = embedding_response(input_text)
        st.markdown(response)


if selected == "Ask Me Anything":
    st.title("👾Ask me a Question❓ ")
    # creating text box
    in_prompt = st.text_area(label="",placeholder="Ask Rocker AI.......")

    if st.button("Get Answer▶️"):
       response = gemini_response(in_prompt)
       st.markdown(response)



