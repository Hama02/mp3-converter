import pika, sys, os, time
from send import email


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()

    def callback(ch, method, properties, body):
        err = email.notification(body)
        if err:
            ch.basic_nack(delivery_tag=method.delivery_tag)
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(
        queue=os.environ.get("MP3_QUEUE"), on_message_callback=callback
    )
    print("Waiting for messages, press CTRL+C to exit")
