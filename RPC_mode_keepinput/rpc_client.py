import pika
import uuid
import sys

class FibnacciRPCClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response,
                                   queue=self.callback_queue,
                                   no_ack=True)

    def on_response(self, ch, method, properties, body):
        if self.corr_id == properties.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange="",
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties(
                                       reply_to = self.callback_queue,
                                       correlation_id = self.corr_id,
                                       ),
                                   body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)
while 1:
    fibonacci_rpc = FibnacciRPCClient()
    i = input("please input a integer:")
    if not i:
        continue
    elif str(i).isdigit():
        i = int(i)
    elif str(i).isalpha() and i == 'q':
        sys.exit(0)
    else:
        print("Input a integer number")
        continue
    print("[x] Requesting fib({})".format(i))
    response = fibonacci_rpc.call(i)
    print("[.]Got %r" % response)
            
                                   
