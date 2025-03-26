import os
import faiss
import ollama
import uvicorn
import fitz  # PyMuPDF for PDFs
import numpy as np
from typing import List
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from sentence_transformers import SentenceTransformer
from PIL import Image
import io

# Initialize FastAPI
app = FastAPI(title="Cybersecurity Content Moderator ")

# Load Sentence Transformer model for embeddings
embedding_model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

# Create FAISS index
dimension = 384  # Embedding size of MiniLM
faiss_index = faiss.IndexFlatL2(dimension)
text_chunks = []  # Store original text chunks
chunk_id_map = {}  # Map FAISS index IDs to text chunks

# Ollama Models
TEXT_MODEL = "cybersecurity-contentmoderator-wizardlm7b"
VISION_MODEL = "cybersecurity-contentmoderator-G3"

def chunk_text(text: str) -> List[str]:
    """Splits text into chunks at sentence level (using '.')"""
    return [sentence.strip() for sentence in text.split(".") if sentence.strip()]

def add_chunks_to_faiss(chunks: List[str]):
    """Embeds text chunks and stores them in FAISS for fast retrieval."""
    global text_chunks
    for chunk in chunks:
        embedding = embedding_model.encode([chunk])
        faiss_index.add(np.array(embedding, dtype=np.float32))
        chunk_id_map[len(text_chunks)] = chunk
        text_chunks.append(chunk)

@app.post("/moderate-text/")
async def moderate_text(content: str = Form(...)):
    """Moderates pasted text using the text-based model."""
    chunks = chunk_text(content)
    add_chunks_to_faiss(chunks)
    results = []
    for chunk in chunks:
        response = ollama.chat(model=TEXT_MODEL, messages=[{"role": "user", "content": chunk}])
        results.append({"chunk": chunk, "moderation_result": response["message"]["content"]})
    return JSONResponse({"moderation_results": results})

@app.post("/moderate-image/")
async def moderate_image(file: UploadFile = File(...)):
    """Processes an uploaded image using the vision-based model."""
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data))
    response = ollama.chat(model=VISION_MODEL, messages=[{"role": "user", "content": "Analyze this image for cybersecurity threats."}], images=[image])
    return JSONResponse({"moderation_result": response["message"]["content"]})

@app.post("/moderate-pdf/")
async def moderate_pdf(file: UploadFile = File(...)):
    """Processes a PDF by extracting text and images, using both models."""
    pdf_text = ""
    images = []
    doc = fitz.open(stream=await file.read(), filetype="pdf")
    for page in doc:
        pdf_text += page.get_text("text") + "\n"
        img_list = page.get_images(full=True)
        for img_index, img in enumerate(img_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            img_bytes = base_image["image"]
            images.append(Image.open(io.BytesIO(img_bytes)))
    
    # Process text using TEXT_MODEL
    text_chunks = chunk_text(pdf_text)
    add_chunks_to_faiss(text_chunks)
    text_results = []
    for chunk in text_chunks:
        response = ollama.chat(model=TEXT_MODEL, messages=[{"role": "user", "content": chunk}])
        text_results.append({"chunk": chunk, "moderation_result": response["message"]["content"]})
    
    # Process images using VISION_MODEL
    image_results = []
    for img in images:
        response = ollama.chat(model=VISION_MODEL, messages=[{"role": "user", "content": "Analyze this image for cybersecurity threats."}], images=[img])
        image_results.append({"moderation_result": response["message"]["content"]})
    
    return JSONResponse({"text_moderation": text_results, "image_moderation": image_results})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
    
#uvicorn backend:app --host 0.0.0.0 --port 8000 --reload
