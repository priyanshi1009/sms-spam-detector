from flask import Flask, render_template, request
import joblib
import csv
import os

from preprocess import clean_text

# -----------------------------
# Load Model & Vectorizer
# -----------------------------
model = joblib.load("models/spam_model.pkl")
vectorizer = joblib.load("models/vectorizer.pkl")

app = Flask(__name__)


# -----------------------------
# Home Page
# -----------------------------
@app.route("/")
def home():

    history = []

    if os.path.exists("history.csv"):

        with open("history.csv", "r", encoding="utf-8") as file:

            reader = csv.reader(file)

            next(reader, None)

            history = list(reader)[-5:]

    history.reverse()

    return render_template(
        "index.html",
        history=history
    )


# -----------------------------
# Prediction
# -----------------------------
@app.route("/predict", methods=["POST"])
def predict():

    # Get Message
    message = request.form["message"]

    # Clean Message
    cleaned_message = clean_text(message)

    # Convert Text to Vector
    data = vectorizer.transform([cleaned_message])

    # Predict
    prediction = model.predict(data)

    # Confidence Score
    probability = model.predict_proba(data)
    confidence = round(max(probability[0]) * 100, 2)

    # Result
    if prediction[0] == 1:
        result = "Spam"
        display_result = f"🚫 Spam Message (Confidence: {confidence}%)"
    else:
        result = "Not Spam"
        display_result = f"✅ Not Spam (Confidence: {confidence}%)"

    # Create Preview for History
    preview = message

    if len(preview) > 45:
        preview = preview[:45] + "..."

    # Save History
    file_exists = os.path.exists("history.csv")

    with open("history.csv", "a", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["Message", "Prediction"])

        writer.writerow([preview, result])

    # Reload History
    history = []

    with open("history.csv", "r", encoding="utf-8") as file:

        reader = csv.reader(file)

        next(reader)

        history = list(reader)[-5:]

    history.reverse()

    return render_template(
        "index.html",
        prediction=display_result,
        history=history
    )


# -----------------------------
# Clear History
# -----------------------------
@app.route("/clear")
def clear():

    if os.path.exists("history.csv"):
        os.remove("history.csv")

    return render_template(
        "index.html",
        history=[]
    )


# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)