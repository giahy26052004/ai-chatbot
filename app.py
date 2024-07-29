from flask import Flask,render_template,request,jsonify
import os
from flask_cors import CORS
import nltk
nltk.download('punkt')
from chat import get_response
app=Flask(__name__)
CORS(app)
@app.route("/",methods=["GET"])
def index_get():
    return render_template("base.html")
@app.post("/predict")
def predict():
    text=request.get_json().get("message")
    response=get_response(text)
    message={"answer":response}
    return jsonify(message)
from waitress import serve
if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=8000)

