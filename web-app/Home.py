import streamlit as st
import os
import requests
import json
import numpy as np
import time
import base64
from PIL import ImageOps
from io import BytesIO
from PIL import Image
import boto3
import botocore
from pathlib import Path
from PIL import Image

from configs import *

version = os.environ.get("WEB_VERSION", "0.1")

if "gen_img" not in st.session_state:
    st.session_state.gen_img = ''

image = Image.open("./img/bedrock.png")
st.image(image, width=80)
st.header("Bedrock Titan Image Generator")

bedrock_api_endpoint = "https://bedrock-runtime.us-east-1.amazonaws.com/"

url = get_parameter(key_txt2img_api_endpoint)
# url = "https://f734vtv1pd.execute-api.us-east-1.amazonaws.com/prod/" # to run streamlit locally

prompt = st.text_area("**Enter Prompt Text**", value = "", 
                           height=20, key="prompt")
process_button = st.button("Generate", type="primary")
st.divider()

gen_img = ''
st.subheader("Generated Image")

if process_button:
    if bedrock_api_endpoint == "" or prompt == "" or url == "":      
        st.error("Please enter a valid endpoint name, API gateway url and prompt!")
    else:
        with st.spinner("generating image..."):
            try:
                r = requests.post(url,json={"text_prompt":prompt, "endpoint_name":bedrock_api_endpoint},timeout=180)
                data = r.json()
                imgresponse = data["image"]
                image_array = [Image.open(BytesIO(base64.b64decode(base64_image))) for base64_image in imgresponse.get("images")]
                st.image(np.array(image_array))

            except requests.exceptions.ConnectionError as errc:
                st.error("Error Connecting:",errc)
                
            except requests.exceptions.HTTPError as errh:
                st.error("Http Error:",errh)
                
            except requests.exceptions.Timeout as errt:
                st.error("Timeout Error:",errt)    
                
            except requests.exceptions.RequestException as err:
                st.error("OOps: Something Else",err)                
                
        st.success("Success!")