from .device_sensor import *
import cv2
def serializer_for_kafka_producer(data):
    data = encode_and_transmit_numpy_array_in_bytes(data)
    return dumps(data).encode("utf-8")
import datetime
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



class Surveillance_Camera(Device_sensor):

    def __init__(self, kafka_producer_ip_port, produce_to_topic, config_data):

        super(Surveillance_Camera, self).__init__(
            config_data['config_data'], 
            serializer_for_kafka_producer, 
            kafka_producer_ip_port, 
            produce_to_topic)





    def get_data(self):


        # cap = cv2.VideoCapture(self.dir_path + "./sensors/dataset/fall_detection/cs4.mp4")

        cap = cv2.VideoCapture(self.config_IP)


        fps = cap.get(cv2.CAP_PROP_FPS)
        print(f"{fps} FPS")

        # s = datetime.datetime.now()

        ret = True
        while(ret):

            ret, frame = cap.read()

            if ret == False:

                break
                # cap = cv2.VideoCapture(self.config_IP)
                # ret, frame = cap.read()



            scale_percent = 10 # percent of original size
            width = int(frame.shape[1] * scale_percent / 100)
            height = int(frame.shape[0] * scale_percent / 100)
            dim = (width, height)
            # resize image
            frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)


            self.send_data(frame)

            # to skip frames window operation
            x = 0
            while(x < 4):
                ret, frame = cap.read()
                x += 1

        # print("total time : ", datetime.datetime.now() - s)
