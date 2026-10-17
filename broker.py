# broker.py
import queue
import time
from datetime import datetime

class MessageBroker:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MessageBroker, cls).__new__(cls)
            cls._instance.topics = {}
        return cls._instance

    def create_topic(self, topic_name):
        if topic_name not in self.topics:
            self.topics[topic_name] = queue.Queue()

    def produce(self, topic_name, message):
        if topic_name not in self.topics:
            self.create_topic(topic_name)
        self.topics[topic_name].put(message)

    def consume(self, topic_name, timeout=1):
        if topic_name in self.topics:
            try:
                return self.topics[topic_name].get(timeout=timeout)
            except queue.Empty:
                return None
        return None

broker = MessageBroker()