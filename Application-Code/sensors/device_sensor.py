from .generic_sensor import *


class Device_sensor(Generic_Sensor):

    def __init__(self, config_ip, serializer_for_kafka_producer, kafka_producer_ip_port, produce_to_topic):

        super(Device_sensor, self).__init__(
            serializer_for_kafka_producer, 
            kafka_producer_ip_port, 
            produce_to_topic)

            
        self.config_IP = config_ip



