from .generic_operator import *
from pandas import Series
import keras
import base64
import time
import pandas as pd
import datetime

def serializer_for_kafka_producer(data):

    return dumps(data).encode('utf-8')


# Convert Base 64 representation to numpy representation
def receive_decode_bytes_to_numpy_array(j_dumps: str) -> np.array:
    # Convert Base 64 representation to byte representation
    compressed_data = b64decode(j_dumps)
    # Read byte array to an Image
    im = Image.open(BytesIO(compressed_data))
    # Return Image to numpy array format
    return np.array(im)


class Human_Activity_Recognition(Generic_Operator):

    def __init__(self, kafka_producer_ip_port, produce_to_topic, consume_from_topic , on_offset_reset, group_Id, config_data):

        super(Human_Activity_Recognition, self).__init__(
            serializer_for_kafka_producer, 
            kafka_producer_ip_port, 
            produce_to_topic, 
            consume_from_topic, 
            on_offset_reset, 
            group_Id,
            config_data)

        

        self.selected_activities = config_data['selected_activities']
        
        

        #ml model for Human activity recognition
        self.model = keras.models.load_model(self.dir_path + '/models/HAR_model')


        # this just for testing
        self.test_labels = pd.read_csv(self.dir_path + "/models/y_test.txt", delim_whitespace=True, header=None).to_numpy().squeeze()
  

        #list of activities
        self.ACTIVITIES = {
            0: 'WALKING',
            1: 'WALKING_UPSTAIRS',
            2: 'WALKING_DOWNSTAIRS',
            3: 'SITTING',
            4: 'STANDING',
            5: 'LAYING',
        }



    def get_data(self):

        acc = 0.0
        preds_list = []
        start = datetime.datetime.now()
        x = 0
        while True:
            for msg in self.consumers['Gyroscope']:
                j_dumps_data = loads(msg.value)


                body_gyro_x = j_dumps_data['body_gyro_x']
                body_gyro_y = j_dumps_data['body_gyro_y']
                body_gyro_z = j_dumps_data['body_gyro_z']

                # print('\n\ngyro\n\n',body_gyro_x)
                break


            for msg1 in self.consumers['Accelerometer']:
                
                
                j_dumps_data = loads(msg1.value)


                            

                body_acc_x = j_dumps_data['body_acc_x']
                body_acc_y = j_dumps_data['body_acc_y']
                body_acc_z = j_dumps_data['body_acc_z']

                total_acc_x = j_dumps_data['total_acc_x']
                total_acc_y = j_dumps_data['total_acc_y']
                total_acc_z = j_dumps_data['total_acc_z']
                # print('\n\nacc\n\n',body_acc_x)

                break

            # add combining all readings and create (128x9) shape array
            # where 128 are the readings(collected in 2.50 seconds) of 9 dimentions/features
            # 9 features : 3-body_acc_xyz, 3-body_gyro_xyz, 3-total_acc_xyz


            data_point = np.array([
                body_acc_x,
                body_acc_y,
                body_acc_z,
                body_gyro_x,
                body_gyro_y,
                body_gyro_z,
                total_acc_x,
                total_acc_y,
                total_acc_z
            ]).transpose()


            #receiving predictions 
            pred_result = self.transfrom(data_point)

            activity_detected = self.ACTIVITIES[pred_result] in self.selected_activities

            #append 'true' if prediction is found in selected_activities list
            preds_list.append(activity_detected)
            
            #if operator is transmiting data then run this
            if self.produce_to_topic != "":
                #sends data after specified time/window
                if (datetime.datetime.now() - start).seconds >= self.time_window:

                    self.send_data({
                        'data_list' : preds_list
                    })
                    start = datetime.datetime.now()
                    preds_list = []
            else: # else print the results to terminal

                #uncomment this if u want to send alert
                if self.alert_message != "" and activity_detected:
                    self.send_alert() 

                else:
                    if activity_detected:
                        print("Activity Detected : ", self.ACTIVITIES[pred_result])
                    print("{0}-Predicted Label : {1} - Ground Truth : {2}".format(x, self.ACTIVITIES[pred_result], self.ACTIVITIES[self.test_labels[x] - 1]))
                    acc += self.ACTIVITIES[pred_result] == self.ACTIVITIES[self.test_labels[x] - 1]
            
            x += 1

            if x == 1000:

                print("Accuracy : ", acc/1000)



            

    def transfrom(self, args = None):

        #adding another dimention to make shape [1x128x9] to feed HAR_model
        data_point = np.expand_dims(args, axis = 0)

        #making predictions
        pred = self.model.predict(data_point)

        #converting pred vector to a label
        label = np.argmax(pred)



        return label

        # print('\n\zahidzahid\n\n')
