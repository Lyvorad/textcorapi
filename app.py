from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configurar Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Cargar instrucciones del archivo
INSTRUCTIONS_FILE = "instruccionesia.txt"

if not os.path.exists(INSTRUCTIONS_FILE):
    raise FileNotFoundError(f"File '{INSTRUCTIONS_FILE}' not found.")

with open(INSTRUCTIONS_FILE, "r", encoding="utf-8") as f:
    INSTRUCCIONES = f.read().strip()

if not INSTRUCCIONES:
    raise ValueError("The file 'instruccionesia.txt' is empty. Please add valid instructions.")

# Crear modelo de Gemini
model = genai.GenerativeModel("gemini-2.5-flash")


# FastAPI
app = FastAPI(title="Mayusc Text Correction")


class TextRequest(BaseModel):
    text: str


@app.post("/correct")
def correct_text(payload: TextRequest):
    text_to_correct = payload.text.strip()

    if not text_to_correct:
        raise HTTPException(status_code=400, detail="Text cannot be empty.")

    try:
        chat = model.start_chat()

        chat.send_message(INSTRUCCIONES)

        response = chat.send_message(
            f"Corrige profesionalmente el siguiente texto:\n\n{text_to_correct}"
        )

        if hasattr(response, "text") and response.text:
            return response.text

        return "Error: empty response from Gemini."

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ping")
def ping():
    return "pong"
