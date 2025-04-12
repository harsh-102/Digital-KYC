import easyocr
from PIL import Image
import numpy as np

def extract_text_from_image(uploaded_file):
    reader = easyocr.Reader(['en'])  # Load English OCR
    image = Image.open(uploaded_file)
    image_np = np.array(image)
    results = reader.readtext(image_np)
    extracted_text = " ".join([res[1] for res in results])
    return extracted_text
import streamlit as st

st.title("Mini KYC Verifier")
st.write("Upload your ID and fill the form. We'll check if it matches!")

uploaded_file = st.file_uploader("Upload ID Card", type=["jpg", "png", "jpeg"])
if uploaded_file:
    extracted_text = extract_text_from_image(uploaded_file)
    st.subheader("Extracted Text from ID:")
    st.write(extracted_text)

    st.subheader("User Input:")
    name_input = st.text_input("Full Name")
    dob_input = st.text_input("Date of Birth (DD/MM/YYYY)")
    id_input = st.text_input("ID Number")

    if st.button("Verify Details"):
        score = 0
        if name_input.lower() in extracted_text.lower():
            score += 1
        if dob_input in extracted_text:
            score += 1
        if id_input in extracted_text:
            score += 1

        st.success(f"Match Score: {score}/3")
        if score == 3:
            st.success("KYC Passed")
        else:
            st.warning("Some info doesn't match")
from deepface import DeepFace

st.subheader("Optional: Upload Selfie for Face Match")
id_face = st.file_uploader("Upload face from ID card", type=["jpg", "jpeg", "png"], key="idface")
selfie = st.file_uploader("Upload your selfie", type=["jpg", "jpeg", "png"], key="selfie")

if id_face and selfie:
    with open("id_face.jpg", "wb") as f:
        f.write(id_face.getbuffer())
    with open("selfie.jpg", "wb") as f:
        f.write(selfie.getbuffer())

    try:
        result = DeepFace.verify("id_face.jpg", "selfie.jpg", enforce_detection=False)
        if result["verified"]:
            st.success(" Face Match Successful")
        else:
            st.error(" Face Match Failed")
    except Exception as e:
        st.error(f"Error: {e}")
