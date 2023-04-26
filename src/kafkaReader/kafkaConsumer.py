import json
from confluent_kafka import Consumer, KafkaError

class KafkaConsumer:
    def __init__(self, topic, group_id):
        self.topic = topic
        self.conf = {
            'bootstrap.servers' : 'localhost:9092',
            'group.id': group_id,
            'auto.offset.reset': 'earliest' 
        }
        self.consumer = Consumer(self.conf)
        self.consumer.subscribe([self.topic])
    
    def read_next_message(self):
        msg = self.consumer.poll(1.0)
        if msg is None:
            return None
        if msg.error():
            print("Consumer error: {}".format(msg.error()))
            return None
        data = json.loads(msg.value())['payload']
        dict_res = {
            'id' : data['id'],
            'hash' : data['hash'],
            'title' : data['title'],
            'url' : data['url'],
            'content' : data['content'],
            'published_at': data['published_at'],
        }
        return dict_res
    
    def __del__(self):
        self.consumer.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.consumer.close()