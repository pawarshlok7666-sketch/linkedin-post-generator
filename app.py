from dotenv import load_dotenv
import os
from flask import Flask, render_template, request
from google import genai

# Load Environment Variables
load_dotenv()

# Flask App
app = Flask(__name__)

# Gemini Client
client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

@app.route("/", methods=["GET", "POST"])
def home():

    generated_post = ""

    if request.method == "POST":

        topic = request.form["topic"]
        tone = request.form["tone"]

        prompt = f"""
        Write a high-quality LinkedIn post about: {topic}

        Tone:
        {tone}

        Requirements:
        - Human and natural tone
        - Strong hook at the beginning
        - Short readable paragraphs
        - Professional and engaging
        - Avoid cringe and buzzwords
        - Keep under 220 words
        - Add 5 relevant hashtags
        """

        try:

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            generated_post = response.text

        except Exception as e:

            generated_post = f"Error: {str(e)}"

    return render_template(
        "index.html",
        generated_post=generated_post
    )

if __name__ == "__main__":
    app.run(debug=True)