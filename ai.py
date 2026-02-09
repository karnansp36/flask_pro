from flask import Blueprint, request, jsonify
import requests
import google.generativeai as genai
from huggingface_hub import InferenceClient
from PIL import Image
import base64
import io
import os
ai_bp = Blueprint('ai', __name__)

# ----------------------------
# CONFIG
# ----------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
HF_API_KEY = os.getenv("HF_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

# -----------------------------------
# 1️⃣ GEMINI TEXT GENERATION ENDPOINT
# -----------------------------------
@ai_bp.route('/generate-text', methods=['GET','POST'])
def generate_text():
    data = request.json
    prompt = data.get('prompt')

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)

        return jsonify({
            "prompt": prompt,
            "response": response.text
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ----------------------------------------------
# 2️⃣ HUGGINGFACE IMAGE GENERATION ENDPOINT
# ----------------------------------------------
@ai_bp.route('/generate-image', methods=['POST'])
def generate_image():
    try:
        data = request.json
        prompt = data.get("prompt")

       
        client = InferenceClient(
            api_key=HF_API_KEY,
        )

        # returns PIL image
        image = client.text_to_image(
            prompt,
            model="stabilityai/stable-diffusion-xl-base-1.0"
        )

        # Convert image to base64
        img_buffer = io.BytesIO()
        image.save(img_buffer, format="PNG")
        img_str = base64.b64encode(img_buffer.getvalue()).decode("utf-8")

        return jsonify({
            "prompt": prompt,
            "image_base64": img_str
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
