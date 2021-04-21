from .virtual_sensor import *
import pandas as pd


def serializer_for_kafka_producer(data):

    return dumps(data).encode('utf-8')

class Heart_Rate(Virtual_Sensor):

    def __init__(self, kafka_producer_ip_port, produce_to_topic, config_data):

        super(Heart_Rate, self).__init__(
            config_data['config_data'], 
            serializer_for_kafka_producer, 
            kafka_producer_ip_port, 
            produce_to_topic)

        self.time_window = 2

    def get_data(self):
        
        data_set=pd.read_csv(self.dir_path + self.file_name)
        data_set.columns=['time_in_sec','HR']

        sec = 1.0
        for x in range(15):

            greater_than = data_set.time_in_sec >= sec
            less_than = data_set.time_in_sec <= sec + 2
            _range = greater_than == less_than


            data_wrt_time = np.array(data_set[_range].HR)

            for data_item in data_wrt_time:
                self.send_data({
                    "data" : data_item
                    })
                
            # print(data_wrt_time.mean(),'\n\n\n')
            sec += self.time_window
            sleep(2)
            
        
        return False