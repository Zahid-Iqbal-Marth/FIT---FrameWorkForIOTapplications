from .virtual_sensor import *
import pandas as pd
import numpy as np
import base64
import time



def serializer_for_kafka_producer(data):

    return dumps(data).encode("utf-8")

# Converts numpy array to base64(string) representation


def encode_and_transmit_numpy_array_in_bytes(numpy_array: np.array) -> str:
    # Create a Byte Stream Pointer
    compressed_file = BytesIO()
    # Use PIL JPEG reduction to save the image to bytes
    Image.fromarray(numpy_array).save(compressed_file, format="JPEG")
    # Set index to start position
    compressed_file.seek(0)
    # Convert the byte representation to base 64 representation for REST Post
    return b64encode(compressed_file.read()).decode()

class Accelerometer(Virtual_Sensor):

    def __init__(self, kafka_producer_ip_port, produce_to_topic, config_data):

        super(Accelerometer, self).__init__(
            config_data['config_data'], 
            serializer_for_kafka_producer, 
            kafka_producer_ip_port, 
            produce_to_topic)



    def get_data(self):
        
        body_acc_x = pd.read_csv(self.dir_path + "/dataset/Accelerometer/body_acc_x_test.txt", delim_whitespace=True, header=None)
        body_acc_y = pd.read_csv(self.dir_path + "/dataset/Accelerometer/body_acc_y_test.txt", delim_whitespace=True, header=None)
        body_acc_z = pd.read_csv(self.dir_path + "/dataset/Accelerometer/body_acc_z_test.txt", delim_whitespace=True, header=None)
        
        total_acc_x = pd.read_csv(self.dir_path + "/dataset/Accelerometer/total_acc_x_test.txt", delim_whitespace=True, header=None)
        total_acc_y = pd.read_csv(self.dir_path + "/dataset/Accelerometer/total_acc_y_test.txt", delim_whitespace=True, header=None)
        total_acc_z = pd.read_csv(self.dir_path + "/dataset/Accelerometer/total_acc_z_test.txt", delim_whitespace=True, header=None)

        x = 0
        time_window = 2.50
        while x < len(body_acc_x):

            if x == 15:
                break

            self.send_data({
                "body_acc_x" : np.array(body_acc_x.loc[x, :]).tolist(),
                "body_acc_y" : np.array(body_acc_y.loc[x, :]).tolist(),
                "body_acc_z" : np.array(body_acc_z.loc[x, :]).tolist(),

                "total_acc_x" : np.array(total_acc_x.loc[x, :]).tolist(),
                "total_acc_y" : np.array(total_acc_y.loc[x, :]).tolist(),
                "total_acc_z" : np.array(total_acc_z.loc[x, :]).tolist(),
                })
                
            x += 1


            # sleep(time_window)
