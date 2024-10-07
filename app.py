import os
import threading
import json
import logging
import uuid
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pika
import nltk
import time

nltk.download('punkt')

app = Flask(__name__)
CORS(app)

# RabbitMQ configuration
rabbitmq_host = 'ecstatic_galois'  # Tên container RabbitMQ

  # Nếu bạn muốn dùng tên container
 # Tên container RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
channel = connection.channel()

# Ensure the queue exists
channel.queue_declare(queue='chatbot')

@app.route("/", methods=["GET"])
def index_get():
    return render_template("base.html")

responses = {}
response_lock = threading.Lock()

def callback(ch, method, properties, body):
    response = json.loads(body.decode())
    with response_lock:
        responses[response['uuid']] = response['response']

def start_consuming():
    channel.basic_consume(queue='chatbot', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

consumer_thread = threading.Thread(target=start_consuming)
consumer_thread.daemon = True
consumer_thread.start()

@app.post("/predict")
def predict():
    try:
        text = request.get_json().get("message")
        message_id = str(uuid.uuid4())  # Tạo uuid cho yêu cầu

        # Gửi tin nhắn tới RabbitMQ
        channel.basic_publish(exchange='', routing_key='chatbot', body=json.dumps({"uuid": message_id, "message": text}))

        # Chờ phản hồi
        for _ in range(10):
            time.sleep(1)
            with response_lock:
                if message_id in responses:
                    response = responses.pop(message_id)
                    return jsonify({"response": response}), 200

        return jsonify({"status": "timeout"}), 408
    except Exception as e:
        logging.error("Error occurred: %s", e)
        return {"error": "Internal server error"}, 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
