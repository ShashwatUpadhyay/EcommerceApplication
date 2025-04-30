# import pika
# import random

# def publish_message(message):
#     params  = pika.URLParameters('amqps://amnlqcfv:dcHiFJCwOrhQXbIofcvvwt6N3JL6J9DA@jaragua.lmq.cloudamqp.com/amnlqcfv')
#     connection = pika.BlockingConnection(params)
#     channel = connection.channel()
#     channel.queue_declare(queue='e_queue')
#     message = f'Hello {random.randint(1, 100)}'
#     channel.basic_publish(exchange='', routing_key='e_queue', body=message)
#     print(f" [x] Sent {message}")
#     connection.close()