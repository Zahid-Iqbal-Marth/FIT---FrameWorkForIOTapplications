from django.contrib.auth.models import User, Group
from rest_framework import viewsets, status
from .serializers import MovieSerializer
from .models import Movie
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import paramiko
from scp import SCPClient
import os

def Home(request):
    return HttpResponse("<h1> Hello Friend <h1>")

@csrf_exempt
def Receive_request(request):

    # print('\n\n\nZahid\n\n\n')

    if request.method == 'POST':
        data = JSONParser().parse(request)
        Generate_Code(data)

        return JsonResponse({'message' : 'Successfully Created'}, status = status.HTTP_201_CREATED)
    else:
        return HttpResponse("<h1> Hello Friend <h1>")

def Generate_Code(data):

  

    class_name_to_file_name = {
        'Surveillance_Camera' : 'surveillance_camera',
        'Heart_Rate' : 'heart_rate_sensor',
        'Edge_detection' : 'edge_detection_operator',
        'Noise_Removel' : 'noise_removel_operator',
        'Filter' : 'heart_rate_filter',
        'Gyroscope' : 'gyroscope',
        'Accelerometer' : 'accelerometer',
        'Human_Activity_Recognition' : 'HAR_operator',
        'Fall_detection' : 'fall_detection_operator',
        'Logical_Operator' : 'logical_operator',

    }


    Name_of_nodes = []



    out_file = open("../../Application-Code/main_file.py", "w")

    #importing thread
    out_file.write("import thread\n")

    #data -> json obj

    # Iterating through the json 
    # iterating to add imports
    for nodes in data:
        if nodes == "Deploy_info":
            break
        location = "{0}.{1}".format(data[nodes]['type'], class_name_to_file_name[data[nodes]['class_name']]) 

        class_name = "{0}".format(data[nodes]['class_name'])

        out_file.write("from {0} import {1}\n".format(location, class_name))


    # adding function, use to initiate process and threads

    out_file.write("def start_consuming_and_producing(component):\n")
    out_file.write("    component.get_data()\n\n")


    # now create objects for the given pipeline
    # iterating to create objects
    #constants 

    on_offset_reset = 'earliest'
    kafka_producer_ip_port = 'localhost:9092'


    for nodes in data: 
        if nodes == "Deploy_info":
            break
        object_name = data[nodes]['class_name'] + "_" + data[nodes]['type']
        class_name = data[nodes]['class_name']
        produce_to_topic = data[nodes]['produce_to_topic']
        config_data = data[nodes]['config_data']
        consume_from_topic = data[nodes]['consume_from_topic']
        consumer_group_id = data[nodes]['id']

        if data[nodes]['type'] == 'sensors':
            out_file.write( "{0} = {1}('{2}','{3}', {4})\n\n".format(object_name, class_name, kafka_producer_ip_port, produce_to_topic, config_data))
        elif data[nodes]['type'] == 'operators':
            out_file.write( "{0} = {1}('{2}','{3}', {4}, '{5}', '{6}', {7})\n\n".format(object_name, class_name, kafka_producer_ip_port, produce_to_topic, consume_from_topic, on_offset_reset, consumer_group_id, config_data))

        Name_of_nodes.append(object_name)

    #now creating threads which will run these objects

    for node in Name_of_nodes:

        out_file.write("thread.start_new_thread( start_consuming_and_producing, ({0}, ) )\n\n".format(node))


    #adding a inf loop 
    out_file.write("while True:\n")
    out_file.write("    pass")



    out_file.close()



    base_dir = "../../"

    deploy_device_ip = data["Deploy_info"]["deploy_device_ip"]
    device_username = data["Deploy_info"]["device_username"]
    device_pass = data["Deploy_info"]["device_pass"]


    append_record_file = open("deploy_record.txt", 'a')
    read_record_file = open("deploy_record.txt", 'r')
    proxy = None
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(deploy_device_ip, username=device_username,password = device_pass, sock=proxy)



    scp = SCPClient(client.get_transport())
    if deploy_device_ip not in read_record_file.read():


        os.system("cd " + base_dir + " && zip -r deployment-matrical Application-Code kafka start_kafka.py setup.sh" )


        scp.put(base_dir + "deployment-matrical.zip", "FIT.zip")
        ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command("unzip FIT.zip -d FIT")
        exit_code = ssh_stdout.channel.recv_exit_status() # handles async exit error 
        # exit_code = ssh_stderr.channel.recv_exit_status() # handles async exit error 


        for line in ssh_stdout:
            print(line.strip())
        # for line in ssh_stderr:
        #     print(line.strip())        

        append_record_file.write(deploy_device_ip+"\n")


    read_record_file.close()
    append_record_file.close()




    scp.put(base_dir + "Application-Code/main_file.py", "FIT/Application-Code/main_file.py")