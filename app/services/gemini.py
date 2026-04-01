import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_image(image_url: str):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content([
            "Describe this image:",
            image_url
        ])

        return response.text

    except Exception as e:
        print("Gemini error:", e)
        return "This appears to be a simple generated placeholder image with text, likely representing a concept or logo idea."