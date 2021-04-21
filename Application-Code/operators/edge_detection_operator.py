from .generic_operator import *
import cv2

def serializer_for_kafka_producer(data):
    data = encode_and_transmit_numpy_array_in_bytes(data)
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


# Convert Base 64 representation to numpy representation
def receive_decode_bytes_to_numpy_array(j_dumps: str) -> np.array:
    # Convert Base 64 representation to byte representation
    compressed_data = b64decode(j_dumps)
    # Read byte array to an Image
    im = Image.open(BytesIO(compressed_data))
    # Return Image to numpy array format
    return np.array(im)








class Edge_detection(Generic_Operator):

    def __init__(self, kafka_producer_ip_port, produce_to_topic, consume_from_topic , on_offset_reset, group_Id, config_data):

        super(Edge_detection, self).__init__(
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

        if len(self.consumers_name_list) == 1:

            for data in self.consumers[self.consumers_name_list[0]]:

                j_dumps_data = loads(data.value)

                img = receive_decode_bytes_to_numpy_array(j_dumps_data)

                self.transfrom(img)



    def transfrom(self, args = None):

        img = args
        img = cv2.Canny(img,self.lower_bound,self.upper_bound)
        cv2.imshow('image', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            exit()


        if self.produce_to_topic != "":
            self.send_data(img)
    


