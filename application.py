from flask import Flask, render_template, request, session
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle

# Initialize the Flask application
application = Flask(__name__) 

# Load application configurations
application.config.from_object(__name__)

# Basic model loading
def load_model():
    loaded_model = None
    with open('basic_classifier.pkl', 'rb') as fid:
        loaded_model = pickle.load(fid)
    return loaded_model

# Count vectorizer model loading
def load_vectorizer():
    vectorizer = None
    with open('count_vectorizer.pkl', 'rb') as vd:
        vectorizer = pickle.load(vd)
    return vectorizer

# Make Predictions
def predict(loaded_model, vectorizer, string):
    # check if input string is valid
    if type(string) == str:
        # use model to predict
        prediction = loaded_model.predict(vectorizer.transform([string]))[0]

        # output prediction mapping
        if prediction == "REAL" or prediction == "FAKE":
            return prediction

    return "INVALID INPUT"

model = load_model()
vectorizer = load_vectorizer()

# Index
@application.route("/", methods=["GET"])
def index():
    headline = request.args.get("query")
    prediction = None
    if headline != None:
        prediction = predict(model, vectorizer, headline)
        return render_template("index.html", headline=headline, prediction=prediction)
    return render_template("index.html")

# Start the Flask app
if __name__ == '__main__':
    application.run(port=5000, debug=True)