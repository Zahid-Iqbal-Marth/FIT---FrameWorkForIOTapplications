from kafka import KafkaProducer
from json import dumps
from time import sleep, time
import numpy as np
from io import BytesIO
from PIL import Image
from base64 import b64encode
import os


class Generic_Sensor:

    def __init__(self, serializer_for_kafka_producer, kafka_producer_ip_port, produce_to_topic):
        
        self.produce_to_topic = produce_to_topic
        # Create a kafka producer
        self.producer = KafkaProducer(
            bootstrap_servers = [kafka_producer_ip_port],
            value_serializer = serializer_for_kafka_producer
        )
        
        self.dir_path = os.path.dirname(os.path.realpath(__file__))

    def delivery_report(err, decoded_message, original_message):
        if err is not None:
            print(err)

    def send_data(self, data):

        self.producer.send(self.produce_to_topic, data) 
        
    # producer.flush()

    def get_data(self):
        #implement it in specifice extended class
        pass

