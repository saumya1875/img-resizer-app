import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io


hide_streamlit_cloud_elements = """
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    a[title="View source"] {display: none !important;}
    button[kind="icon"] {display: none !important;}
    </style>
"""
st.markdown(hide_streamlit_cloud_elements, unsafe_allow_html=True)

st.header("Welcome to Image Resizer")

uploaded_image = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

if uploaded_image:
    img = Image.open(uploaded_image)
    array_image = np.array(img)
    st.image(array_image, caption="Original Image",  use_container_width=100)

    # Resize controls
    width = st.number_input("Enter width", min_value=1, value=array_image.shape[1])
    height = st.number_input("Enter height", min_value=1, value=array_image.shape[0])

    # Flip option
    flip_value = st.selectbox("Direction", ["None", "Vertical", "Horizontal"])

    if flip_value == "Vertical":
        array_image = cv2.flip(array_image, 0)
    elif flip_value == "Horizontal":
        array_image = cv2.flip(array_image, 1)

    st.image(array_image, caption="Flipped Image", width=100)

    # Resize and download
    if st.button("Resize Image"):
        resized_image = cv2.resize(array_image, (int(width), int(height)))
        st.image(resized_image, caption="Resized Image", width=100)

        buff = io.BytesIO()
        pil_img = Image.fromarray(resized_image)
        pil_img.save(buff, format="JPEG")

        st.download_button(
            "Download here",data=buff.getvalue(),mime="image/jpeg",file_name="resized_image.jpeg")
