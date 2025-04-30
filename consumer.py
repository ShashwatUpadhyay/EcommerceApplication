# import pika

# def callback(ch, method, properties, body):
#     print(f" [x] Received {body.decode()}")
    

# params  = pika.URLParameters('amqps://amnlqcfv:dcHiFJCwOrhQXbIofcvvwt6N3JL6J9DA@jaragua.lmq.cloudamqp.com/amnlqcfv')
# connection = pika.BlockingConnection(params)
# channel = connection.channel()
# channel.queue_declare(queue='e_queue')
# channel.basic_consume(queue='e_queue', on_message_callback=callback, auto_ack=True)
# channel.start_consuming()
