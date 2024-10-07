import pika
from chat import get_response

def callback(ch, method, properties, body):
    text = body.decode()
    response = get_response(text)  # Gọi hàm xử lý văn bản
    print(f"Received: {text}, Responded: {response}")

def start_consumer():
    rabbitmq_host = 'localhost'  # Thay đổi nếu cần
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()

    channel.queue_declare(queue='chatbot')

    channel.basic_consume(queue='chatbot', on_message_callback=callback, auto_ack=True)

    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    start_consumer()
