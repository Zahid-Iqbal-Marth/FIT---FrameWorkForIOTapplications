from .generic_operator import *
import cv2
import time
import datetime

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








class Fall_detection(Generic_Operator):

    def __init__(self, kafka_producer_ip_port, produce_to_topic, consume_from_topic , on_offset_reset, group_Id, config_data):

        super(Fall_detection, self).__init__(
            serializer_for_kafka_producer, 
            kafka_producer_ip_port, 
            produce_to_topic, 
            consume_from_topic, 
            on_offset_reset, 
            group_Id,
            config_data)



    def get_data(self):

        j = 0
        fgbg = cv2.createBackgroundSubtractorMOG2()








        start = datetime.datetime.now()

        result_list = []
        if len(self.consumers_name_list) == 1:

            for data in self.consumers[self.consumers_name_list[0]]:

                j_dumps_data = loads(data.value)

                img = receive_decode_bytes_to_numpy_array(j_dumps_data)

                j, fgbg, result, frame = self.transfrom([img, fgbg, j])
                result_list.append(result)

                
                if self.produce_to_topic != "":
                    #sends data after specified time/window
                    if (datetime.datetime.now() - start).seconds >= self.time_window:
                       
                        self.send_data({
                            'data_list' : result_list
                        })
                        start = datetime.datetime.now()
                        filtered_list = []

                else:

                    if result:
                        if self.alert_message != "" :
                            self.send_alert()
                        print("FALL")
                    else:
                        print("NO FALL")


                    scale_percent = 500 # percent of original size
                    width = int(frame.shape[1] * scale_percent / 100)
                    height = int(frame.shape[0] * scale_percent / 100)
                    dim = (width, height)
                    # resize image
                    frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)

                    cv2.imshow('video', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        cv2.destroyAllWindows()
                        exit()




    def transfrom(self, args = None):

        frame = args[0]
        fgbg = args[1]
        j = args[2]

        result = None

        # print(j)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        fgmask = fgbg.apply(gray)
        #Find contours
        contours, _ = cv2.findContours(fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
        
            # List to hold all areas
            areas = []

            for contour in contours:
                ar = cv2.contourArea(contour)
                areas.append(ar)
            
            max_area = max(areas, default = 0)

            max_area_index = areas.index(max_area)

            cnt = contours[max_area_index]

            M = cv2.moments(cnt)
            
            x, y, w, h = cv2.boundingRect(cnt)


            cv2.drawContours(fgmask, [cnt], 0, (255,255,255), 3, maxLevel = 0)
            
            if h < w:
                j += 1
                
            if j > 10:
                # print("FALL")
                #cv2.putText(fgmask, 'FALL', (x, y), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255,255,255), 2)
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
                result = True
            if h > w:
                j = 0 
                result = False
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

        

        return j, fgbg, result, frame
