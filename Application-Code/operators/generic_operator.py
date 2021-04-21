from kafka import KafkaConsumer, KafkaProducer
from cv2 import imshow, destroyAllWindows, waitKey, resize
from time import time, sleep
from io import BytesIO
from PIL import Image
import numpy as np
from json import loads, dumps
from base64 import b64decode
import os 
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



class Generic_Operator:

    def __init__(self, serializer_for_kafka_producer, kafka_producer_ip_port, produce_to_topic, consume_from_topic, on_offset_reset, group_Id, config_data):

        self.produce_to_topic = produce_to_topic
        
        self.consume_from_topic = consume_from_topic

        self.alert_message = config_data['alert_message']

        self.alert_dest =  config_data['alert_dest']

        self.time_window = config_data['time_window']


        ##code for multi consumer

        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        
        self.consumers = {}
        self.consumers_name_list = []


        for x, consumer in enumerate(self.consume_from_topic):

            # print(consumer)

            consumer_name = consumer.split('-')[1]
            self.consumers_name_list.append(consumer_name)
            
            self.consumers[consumer_name] = KafkaConsumer(
                consumer,
                bootstrap_servers = kafka_producer_ip_port,
                auto_offset_reset = on_offset_reset,
                group_id = group_Id + str(x)
            )

        self.producer = KafkaProducer(
            bootstrap_servers = [kafka_producer_ip_port],
            value_serializer = serializer_for_kafka_producer
        )


    def delivery_report(err, decoded_message, original_message):
        if err is not None:
            print(err)
            

    def send_data(self, data):

        self.producer.send(self.produce_to_topic, data) 




    def get_data(self):
        #implement it in specifice extended class
        pass

    def transfrom(self, args = None):
        #implement it in specifice extended class
        pass

    def send_alert(self):


        #email data
        username = "fitframeworkforiot@gmail.com"
        password = "fit123!@#"


        body = self.alert_message
        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = username
        message["To"] = self.alert_dest
        message["Subject"] = "Alert"

        # Add body to email
        message.attach(MIMEText(body, "plain"))


        text = message.as_string()

        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(username,password)

        server.sendmail(username, self.alert_dest, text)


