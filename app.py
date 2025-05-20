from flask import Flask, render_template, request
import random
import re
from typing import List
import os

app = Flask(__name__)


# Lists of humanizing elements
CONVERSATIONAL_PHRASES = [
    "To be precise, ",
    "It is worth noting that, ",
    "From a practical standpoint, ",
    "Notably, ",
    "To clarify, ",
    "In my professional opinion, ",
    "For context, ",
    "Significantly, ",
    "To begin with, ",
    "From an analytical perspective, ",
    "Importantly, ",
    "To put it into perspective, ",
    "As evidence suggests, ",
    "In practice, ",
    "To illustrate, ",
    "From a strategic viewpoint, ",
    "It should be emphasized that, ",
    "In the interest of clarity, ",
    "As a starting point, ",
    "From an objective standpoint, ",
    "To provide context, ",
    "It is evident that, ",
    "In terms of, ",
    "To shed light on this, ",
    "From a broader perspective, ",
    "To underscore this, ",
    "As research indicates, ",
    "In a professional capacity, ",
    "To frame this discussion, ",
    "It is apparent that, ",
    "From a theoretical angle, ",
    "To highlight, ",
    "As a matter of fact, ",
    "In light of this, ",
    "To set the stage, ",
    "From a critical perspective, ",
    "To provide insight, ",
    "It stands to reason that, ",
    "In the context of, ",
    "To emphasize, ",
    "As data suggests, ",
    "From a pragmatic angle, ",
    "To offer clarity, ",
    "In a practical sense, ",
    "To draw attention to, ",
    "From an evidence-based view, ",
    "To put it another way, ",
    "As a key point, ",
    "In the grand scheme of things, ",
    "To be clear, "
]

TRANSITIONAL_PHRASES = [
    "Furthermore, ",
    "In addition, ",
    "However, ",
    "Conversely, ",
    "Moreover, ",
    "To expand on this, ",
    "In contrast, ",
    "Additionally, ",
    "From another perspective, ",
    "Building on this, ",
    "Consequently, ",
    "To elaborate, ",
    "On a related note, ",
    "In light of this, ",
    "Subsequently, ",
    "As a result, ",
    "On the contrary, ",
    "To build upon this, ",
    "In a similar vein, ",
    "That being said, ",
    "To further this point, ",
    "By contrast, ",
    "In this regard, ",
    "To add to this, ",
    "On the other hand, ",
    "As such, ",
    "To illustrate further, ",
    "In turn, ",
    "Despite this, ",
    "To clarify further, ",
    "In the same way, ",
    "As a consequence, ",
    "To put it differently, ",
    "In parallel, ",
    "To continue this thought, ",
    "On this basis, ",
    "In response to this, ",
    "To complement this, ",
    "As an extension, ",
    "In comparison, ",
    "To build on that idea, ",
    "In this context, ",
    "To elaborate further, ",
    "As a follow-up, ",
    "In conjunction with this, ",
    "To contrast, ",
    "As an additional point, ",
    "In line with this, ",
    "To reinforce this, ",
    "Correspondingly, "
]

HUMAN_QUIRKS = [
    "in essence",
    "broadly speaking",
    "to some extent",
    "in practical terms",
    "as it stands",
    "by and large",
    "in the broader context",
    "to a certain degree",
    "from a certain angle",
    "in principle",
    "on balance",
    "in retrospect",
    "for all intents and purposes",
    "in a broader sense",
    "to put it succinctly",
    "in general terms",
    "at its core",
    "in the final analysis",
    "to a large extent",
    "in effect",
    "as a general rule",
    "in the main",
    "for the most part",
    "in a sense",
    "by all accounts",
    "to all appearances",
    "in practical reality",
    "at the heart of it",
    "in the long run",
    "as a whole",
    "in summary",
    "to an extent",
    "in broad strokes",
    "at its essence",
    "in the overall scheme",
    "by way of summary",
    "in a manner of speaking",
    "to some degree",
    "in the larger context",
    "as a practical matter",
    "in the grand scheme",
    "to encapsulate",
    "in fundamental terms",
    "by most measures",
    "in a wider sense",
    "to summarize",
    "in real terms",
    "at the end of the analysis",
    "in conceptual terms",
    "as a key consideration"
]


# Function to split text into paragraphs
def split_into_paragraphs(text: str) -> List[str]:
    return text.split('\n\n')


# Function to add conversational phrases
def add_conversational_tone(paragraph: str) -> str:
    sentences = re.split(r'(?<=[.!?])\s+', paragraph.strip())
    if not sentences:
        return paragraph

    # Randomly decide to add a conversational phrase to the first sentence
    if random.random() < 0.9:  # 30% chance
        sentences[0] = random.choice(CONVERSATIONAL_PHRASES) + sentences[0].lower()

    # Randomly add transitional phrases between sentences
    for i in range(1, len(sentences)):
        if random.random() < 0.9:  # 20% chance
            sentences[i] = random.choice(TRANSITIONAL_PHRASES) + sentences[i].lower()

    return ' '.join(sentences)


# Function to add slight imperfections and quirks
def add_quirks(text: str) -> str:
    words = text.split()
    for i in range(len(words)):
        if random.random() < 0.9:  # 10% chance to add a quirk
            if words[i].endswith('.') or words[i].endswith('!') or words[i].endswith('?'):
                if random.random() < 0.9:  # 50% chance to add quirk after punctuation
                    words[i] = words[i][:-1] + f", {random.choice(HUMAN_QUIRKS)}{words[i][-1]}"
    return ' '.join(words)


# Function to vary sentence length
def vary_sentence_length(paragraph: str) -> str:
    sentences = re.split(r'(?<=[.!?])\s+', paragraph.strip())
    if not sentences:
        return paragraph

    new_sentences = []
    for i, sentence in enumerate(sentences):
        if random.random() < 0.9 and i < len(sentences) - 1:  # 30% chance to combine sentences
            new_sentences.append(sentence.strip() + ' and ' + sentences[i + 1].lower())
            sentences[i + 1] = ''  # Mark for removal
        else:
            new_sentences.append(sentence)

    # Filter out empty sentences
    new_sentences = [s for s in new_sentences if s]
    return ' '.join(new_sentences)


# Main function to humanize the article
def humanize_article(text: str) -> str:
    paragraphs = split_into_paragraphs(text)
    humanized_paragraphs = []

    for paragraph in paragraphs:
        if not paragraph.strip():
            continue
        # Apply transformations
        paragraph = add_conversational_tone(paragraph)
        paragraph = vary_sentence_length(paragraph)
        paragraph = add_quirks(paragraph)
        humanized_paragraphs.append(paragraph)

    return '\n\n'.join(humanized_paragraphs)



@app.route('/', methods=['GET', 'POST'])
def index():
    output = ""
    if request.method == 'POST':
        input_text = request.form.get('input_text', '')
        if input_text.strip():
            output = humanize_article(input_text)
    return render_template('index.html', output=output)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
