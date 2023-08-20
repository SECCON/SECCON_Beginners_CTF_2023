import os
import uuid
from admin import share2admin
from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return open("./index.html").read()

@app.route("/", methods=["POST"])
def chall():
    try:
        text = request.json["text"]
    except Exception:
        return {"message": "text is required."}
    fileId = uuid.uuid4()
    file_path = f"/var/www/uploads/{fileId}.html"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f'<p style="font-size:30px">{text}</p>')
    message, ocr_url, input_url = share2admin(text, fileId)
    os.remove(file_path)
    return {"message": message, "ocr_url": ocr_url, "input_url": input_url}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
