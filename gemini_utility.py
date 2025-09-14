import os
import json


import google.generativeai as genai


# get the working directory
Working_directory = os.path.dirname(os.path.abspath(__file__))

config_file_path = f"{Working_directory}/config.json"
config_data = json.load(open(config_file_path))

# loading the api key
GOOGLE_API_KEY = config_data["GOOGLE_API_KEY"]

# configuring google.generativeai with API key
genai.configure(api_key=GOOGLE_API_KEY)
# fxn to load gemini-pro model for chatbot


def load_model():
    rocker_model = genai.GenerativeModel("gemini-2.5-flash")
    return rocker_model
# fxn for image captioning


def load_vision_model(prompt, image):
    vision_model = genai.GenerativeModel("gemini-2.5-flash-lite")
    response = vision_model.generate_content([prompt, image])
    result = response.text
    return result

# getting embedding of a given text

def embedding_response(input_text):
    embedding_model = "models/gemini-embedding-001"
    embedding = genai.embed_content(model=embedding_model,
                                    content=input_text,
                                    task_type='retrieval_document')
    embedding_list = embedding['embedding']
    return embedding_list


def gemini_response(in_prompt):
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(in_prompt)
    result = response.text
    return result

















