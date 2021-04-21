from .generic_sensor import *


class Virtual_Sensor(Generic_Sensor):

    def __init__(self, file_name, serializer_for_kafka_producer, kafka_producer_ip_port, produce_to_topic):

        super(Virtual_Sensor, self).__init__(
            serializer_for_kafka_producer, 
            kafka_producer_ip_port, 
            produce_to_topic)
            
        self.file_name = file_name





