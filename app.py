from flask import Flask, render_template, request
import openai
import spacy
import os
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
load_dotenv()
import requests

app = Flask(__name__)

PING_URL = "https://your-app-name.onrender.com/"

def keep_alive():
    try:
        response = requests.get(PING_URL)
        print(f"[Keep Alive] Status: {response.status_code}")
    except Exception as e:
        print(f"[Keep Alive] Failed: {e}")

# Schedule the job every 10 minutes
scheduler = BackgroundScheduler()
scheduler.add_job(func=keep_alive, trigger="interval", minutes=10)
scheduler.start()

# Shut down scheduler when exiting the app
import atexit
atexit.register(lambda: scheduler.shutdown())

def spaCy_cleanup(text: str) -> str:
    """Use spaCy to ensure sentences are well-formed and extract key ideas."""
    doc = nlp(text)
    cleaned_sentences = []

    for sent in doc.sents:
        cleaned = sent.text.strip()
        if len(cleaned.split()) >= 3:
            cleaned_sentences.append(cleaned)

    return " ".join(cleaned_sentences)


def gpt_humanize(text: str) -> str:
    """Use GPT to rewrite and humanize the text."""
    prompt = (
        "Take the following AI-generated text and rewrite it to sound more natural, human-like, and conversational. "
        "Use richer sentence structures, transitional phrases, and ensure coherence:\n\n"
        f"{text}\n\n"
        "Rewritten version:"
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # or "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "You are a helpful and articulate writing assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.85,
            max_tokens=1200,
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"GPT Humanization failed: {e}"


def hybrid_humanize(text: str, as_html=False) -> str:
    """Combine spaCy preprocessing and GPT humanization."""
    cleaned = spaCy_cleanup(text)

    if not cleaned or len(cleaned.split()) < 10:
        return "Text too short or unprocessable."

    humanized = gpt_humanize(cleaned)

    if as_html:
        paragraphs = humanized.split("\n")
        return '\n\n'.join(f"<p>{p.strip()}</p>" for p in paragraphs if p.strip())
    else:
        return humanized

@app.route('/', methods=['GET', 'POST'])
def index():
    output = ""
    if request.method == 'POST':
        input_text = request.form.get('input_text', '')
        if input_text.strip():
            output = hybrid_humanize(input_text, as_html=True)
    return render_template('index.html', output=output)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)

