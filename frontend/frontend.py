import streamlit as st
import requests
from PIL import Image
import io

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
                st.write("### 🚀 Moderation Results:")
                for res in results:
                    st.markdown(f"**Chunk:** {res['chunk']}")
                    st.code(res["moderation_result"], language="json")
            else:
                st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
                st.write("🔍 API Response Debug:", response.text)  # Debugging output
        else:
            st.warning("⚠️ Please enter text for moderation.")

elif input_type == "Upload PDF":
    st.subheader("📄 Upload PDF for Moderation")
    uploaded_pdf = st.file_uploader("Choose a PDF file", type=["pdf"])
    
    if uploaded_pdf and st.button("Moderate PDF"):
        files = {"file": (uploaded_pdf.name, uploaded_pdf.getvalue(), "application/pdf")}
        response = requests.post(f"{API_URL}/moderate-pdf/", files=files)

        if response.status_code == 200:
            results = response.json()
            
            # 🔹 Text Moderation Results
            if "text_moderation" in results and results["text_moderation"]:
                st.write("### 📝 Text Moderation Results:")
                for res in results["text_moderation"]:
                    st.markdown(f"**Chunk:** {res['chunk']}")
                    st.code(res["moderation_result"], language="json")
            else:
                st.warning("⚠️ No text detected in the PDF.")

            # 🔹 Image Moderation Results
            if "image_moderation" in results and results["image_moderation"]:
                st.write("### 🖼️ Image Moderation Results:")
                for res in results["image_moderation"]:
                    if "moderation_result" in res:
                        st.code(res["moderation_result"], language="json")
                    else:
                        st.error("⚠️ Error: Missing 'moderation_result' key in response.")
            
                # Display Extracted Images
                st.write("### 📷 Extracted Images from PDF:")
                for res in results["image_moderation"]:
                    if "image_path" in res:
                        image_response = requests.get(f"{API_URL}/{res['image_path']}")  # Fetch image
                        if image_response.status_code == 200:
                            img = Image.open(io.BytesIO(image_response.content))
                            st.image(img, caption=res["image_path"], use_column_width=True)
                        else:
                            st.warning(f"⚠️ Could not fetch image: {res['image_path']}")
            else:
                st.warning("⚠️ No images found in the PDF.")
        
        else:
            st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
            st.write("🔍 API Response Debug:", response.text)  # Debugging output

elif input_type == "Upload Image":
    st.subheader("📷 Upload Image for Moderation")
    uploaded_image = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])
    
    if uploaded_image and st.button("Moderate Image"):
        files = {"file": (uploaded_image.name, uploaded_image.getvalue(), "image/png")}
        response = requests.post(f"{API_URL}/moderate-image/", files=files)

        if response.status_code == 200:
            result = response.json()
            if "moderation_result" in result:
                st.write("### 🖼️ Image Moderation Result:")
                st.code(result["moderation_result"], language="json")
            else:
                st.error("⚠️ Missing 'moderation_result' in API response.")
            
            # Display Uploaded Image
            image = Image.open(uploaded_image)
            st.image(image, caption="Uploaded Image", use_column_width=True)
        
        else:
            st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
            st.write("🔍 API Response Debug:", response.text)  # Debugging output
