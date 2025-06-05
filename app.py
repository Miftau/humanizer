from flask import Flask, render_template, request
import random
import re
from typing import List
import os

app = Flask(__name__)

# Humanizing Elements
CONVERSATIONAL_PHRASES = [
    "To be precise, ", "It is worth noting that, ", "Notably, ", "To clarify, ", "For context, ",
    "In practice, ", "To illustrate, ", "From an analytical perspective, ", "Importantly, ",
    "As evidence suggests, ", "To put it into perspective, ", "In the interest of clarity, ",
    "From a broader perspective, ", "To underscore this, ", "In a professional capacity, ",
    "To frame this discussion, ", "It is apparent that, ", "To highlight, ",
    "In light of this, ", "To set the stage, ", "From a critical perspective, ",
    "To emphasize, ", "In the context of, ", "To offer clarity, ", "In a practical sense, ",
    "To draw attention to, ", "To put it another way, ", "In the grand scheme of things, ", "To be clear, "
]

TRANSITIONAL_PHRASES = [
    "Furthermore, ", "In addition, ", "However, ", "Moreover, ", "To expand on this, ",
    "In contrast, ", "Additionally, ", "From another perspective, ", "Consequently, ",
    "To elaborate, ", "On a related note, ", "Subsequently, ", "As a result, ",
    "On the contrary, ", "In a similar vein, ", "That being said, ", "By contrast, ",
    "To add to this, ", "On the other hand, ", "As such, ", "To illustrate further, ",
    "In this context, ", "As an additional point, ", "To reinforce this, "
]

HUMAN_QUIRKS = [
    "in essence", "to some extent", "as it stands", "by and large", "in principle",
    "on balance", "in retrospect", "for all intents and purposes", "to put it succinctly",
    "in general terms", "at its core", "in effect", "as a general rule", "to an extent",
    "in broad strokes", "at its essence", "in a manner of speaking", "to some degree",
    "as a practical matter", "in the grand scheme", "to encapsulate", "by most measures",
    "in a wider sense", "to summarize", "at the end of the analysis"
]


def split_into_paragraphs(text: str) -> List[str]:
    """Split text into logical paragraphs, ignoring excess whitespace."""
    return re.split(r'\n\s*\n', text.strip())


def add_conversational_tone(paragraph: str) -> str:
    sentences = re.split(r'(?<=[.!?])\s+', paragraph.strip())
    if not sentences:
        return paragraph

    if random.random() < 0.9:
        sentences[0] = random.choice(CONVERSATIONAL_PHRASES) + sentences[0][0].lower() + sentences[0][1:]

    for i in range(1, len(sentences)):
        if random.random() < 0.9:
            sentences[i] = random.choice(TRANSITIONAL_PHRASES) + sentences[i][0].lower() + sentences[i][1:]

    return ' '.join(sentences)


def add_quirks(text: str) -> str:
    words = text.split()
    for i in range(len(words)):
        if random.random() < 0.9:
            if words[i][-1] in '.!?':
                words[i] = words[i][:-1] + f", {random.choice(HUMAN_QUIRKS)}{words[i][-1]}"
    return ' '.join(words)


def vary_sentence_length(paragraph: str) -> str:
    sentences = re.split(r'(?<=[.!?])\s+', paragraph.strip())
    new_sentences = []
    skip_next = False

    for i in range(len(sentences)):
        if skip_next:
            skip_next = False
            continue
        if i < len(sentences) - 1 and random.random() < 0.9:
            combined = sentences[i].strip() + ' and ' + sentences[i + 1].strip().lower()
            new_sentences.append(combined)
            skip_next = True
        else:
            new_sentences.append(sentences[i].strip())

    return ' '.join(new_sentences)


def humanize_article(text: str, as_html=False) -> str:
    paragraphs = split_into_paragraphs(text)
    humanized_paragraphs = []

    for paragraph in paragraphs:
        if not paragraph.strip():
            continue
        paragraph = add_conversational_tone(paragraph)
        paragraph = vary_sentence_length(paragraph)
        paragraph = add_quirks(paragraph)
        humanized_paragraphs.append(paragraph)

    if as_html:
        return '\n\n'.join(f"<p>{p.strip()}</p>" for p in humanized_paragraphs)
    else:
        return '\n\n'.join(humanized_paragraphs)


@app.route('/', methods=['GET', 'POST'])
def index():
    output = ""
    if request.method == 'POST':
        input_text = request.form.get('input_text', '')
        if input_text.strip():
            output = humanize_article(input_text, as_html=True)
    return render_template('index.html', output=output)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)

