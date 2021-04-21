from .generic_operator import *
from pandas import Series
# import time

def serializer_for_kafka_producer(data):

    return data


class Logical_Operator(Generic_Operator):

    def __init__(self, kafka_producer_ip_port, produce_to_topic, consume_from_topic , on_offset_reset, group_Id, config_data):

        super(Logical_Operator, self).__init__(
            serializer_for_kafka_producer, 
            kafka_producer_ip_port, 
            produce_to_topic, 
            consume_from_topic, 
            on_offset_reset, 
            group_Id,
            config_data)

        self.type = config_data['type']
        
    def get_data(self):

        
        while True:
            results_list = []
            for consumer in self.consumers_name_list:

                for msg in self.consumers[consumer]:

                    j_dumps_data = loads(msg.value)

                    data_list = j_dumps_data['data_list']

                    results_list.append((len(data_list) - sum(data_list)) <= len(data_list)/2.0)
                    break

            
            # print("result : ", results_list)

            output = self.transfrom(results_list)

            # print("output : ", output)

            if self.produce_to_topic !="":

                #produce to the topic
                pass
            
            else: #gen alert of print on console
                if output:
                    # uncomment this if u want to send alert
                    if self.alert_message != "":
                        self.send_alert()
                    print("Critical")
                else:
                    print("Normal")
                

            


    def transfrom(self, args = None):

        if self.type == 'AND':
            return sum(args) == len(args)
        elif self.type == 'OR':
            return sum(args) >= 1
