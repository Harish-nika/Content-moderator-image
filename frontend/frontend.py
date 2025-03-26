import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Cybersecurity Content Moderator", layout="wide")
st.title("🔍 Cybersecurity Content Moderator")

# Sidebar for input selection
st.sidebar.header("Select Input Type")
input_type = st.sidebar.radio("Choose an option:", ["Paste Text", "Upload PDF", "Upload Image"])

if input_type == "Paste Text":
    st.subheader("📝 Enter Text for Moderation")
    text_input = st.text_area("Paste text here:", height=200)
    if st.button("Moderate Text"):
        if text_input.strip():
            response = requests.post(f"{API_URL}/moderate-text/", data={"content": text_input})
            if response.status_code == 200:
                results = response.json()["moderation_results"]
                for res in results:
                    st.markdown(f"**Chunk:** {res['chunk']}")
                    st.code(res["moderation_result"], language="json")
            else:
                st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
        else:
            st.warning("Please enter text for moderation.")

elif input_type == "Upload PDF":
    st.subheader("📄 Upload PDF for Moderation")
    uploaded_pdf = st.file_uploader("Choose a PDF file", type=["pdf"])
    if uploaded_pdf and st.button("Moderate PDF"):
        files = {"file": uploaded_pdf.getvalue()}
        response = requests.post(f"{API_URL}/moderate-pdf/", files=files)
        if response.status_code == 200:
            results = response.json()
            st.write("### 📝 Text Moderation Results:")
            for res in results["text_moderation"]:
                st.markdown(f"**Chunk:** {res['chunk']}")
                st.code(res["moderation_result"], language="json")
            st.write("### 🖼️ Image Moderation Results:")
            for res in results["image_moderation"]:
                st.code(res["moderation_result"], language="json")
        else:
            st.error(f"Error: {response.json().get('detail', 'Unknown error')}")

elif input_type == "Upload Image":
    st.subheader("🖼️ Upload Image for Moderation")
    uploaded_image = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])
    if uploaded_image and st.button("Moderate Image"):
        files = {"file": uploaded_image.getvalue()}
        response = requests.post(f"{API_URL}/moderate-image/", files=files)
        if response.status_code == 200:
            result = response.json()["moderation_result"]
            st.code(result, language="json")
        else:
            st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
#streamlit run frontend.py
