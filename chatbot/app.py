import random
from flask import Flask, redirect, render_template, request, url_for
import numpy as np
from tensorflow.keras.models import load_model
import json
import pickle
from nltk.stem import WordNetLemmatizer
import nltk
nltk.download('punkt')
nltk.download('wordnet')


app = Flask(__name__)

# Load the trained model and other necessary files
model = load_model('delta_model.h5')
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
with open('bot.json', 'r') as file:
    data = json.load(file)

# Initialize WordNet Lemmatizer
lemmatizer = WordNetLemmatizer()

def clean_up_sentence(sentence):
    # Tokenize the pattern
    sentence_words = nltk.word_tokenize(sentence)
    # Stemming each word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bow(sentence, words, show_details=True):
    # Tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # Bag of words
    bag = [0]*len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # Filter out predictions below a threshold
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    # Sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

@app.route('/')
def index():
    return render_template('chatbot.html')

@app.route("/get_response", methods=["POST"])
def get_response():
    message = request.form["message"]
    ints = predict_class(message, model)
    response = ''
    for i in data["intents"]:
        if i["tag"] == ints[0]["intent"]:
            response = random.choice(i["responses"])
            break
    return response

if __name__ == "__main__":
    app.run(debug=True,port=4563)
