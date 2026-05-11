from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

from pdf_ai import ask_pdf

app = Flask(__name__)

CORS(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    user_message = request.json["message"]

    answer = ask_pdf(user_message)

    return jsonify({
        "answer": answer
    })


if __name__ == "__main__":
    app.run(debug=True)