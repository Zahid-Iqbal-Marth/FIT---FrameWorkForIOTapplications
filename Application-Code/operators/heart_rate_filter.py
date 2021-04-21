from .generic_operator import *
import datetime


def serializer_for_kafka_producer(data):

    return dumps(data).encode('utf-8')


class Filter(Generic_Operator):

    def __init__(self, kafka_producer_ip_port, produce_to_topic, consume_from_topic , on_offset_reset, group_Id, config_data):

        super(Filter, self).__init__(
            serializer_for_kafka_producer, 
            kafka_producer_ip_port, 
            produce_to_topic, 
            consume_from_topic, 
            on_offset_reset, 
            group_Id,
            config_data)

        self.lower_bound = config_data['lower_bound']
        self.upper_bound = config_data['upper_bound']

    def get_data(self):

        start = datetime.datetime.now()
        filtered_list = []
        if len(self.consumers_name_list) == 1:

            for msg in self.consumers[self.consumers_name_list[0]]:

                j_dumps_data = loads(msg.value)

                data_wrt_time = j_dumps_data['data']
                filtered = self.transfrom(data_wrt_time)
                filtered_list.append(filtered)


                #if operater is not transmitting its value then print the results on console
                #here i'll embed the code for alter
                if self.produce_to_topic == "":

                    if filtered:
                        #uncomment this if u want to send alert
                        if self.alert_message != "" :
                            self.send_alert()
                        print("Heart Rate is  Critical")
                    else:
                        print("Heart Rate is Normal")

                else:
                    #sends data after specified time/window
                    if (datetime.datetime.now() - start).seconds >= self.time_window:
                       
                        self.send_data({
                            'data_list' : filtered_list
                        })
                        start = datetime.datetime.now()
                        filtered_list = []



            


    def transfrom(self, args = None):


        return (args <= self.lower_bound or args >= self.upper_bound)

