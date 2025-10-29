import pika

def get_connection():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="rabbitmq", port=5672)
    )
    return connection

def send_to_queue(message: str):
    connection = get_connection()
    channel = connection.channel()
    channel.queue_declare(queue="scrape_tasks", durable=True)
    channel.basic_publish(
        exchange="",
        routing_key="scrape_tasks",
        body=message.encode(),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        )
    )
    connection.close()
