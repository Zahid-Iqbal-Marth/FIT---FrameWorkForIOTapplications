import paramiko
from scp import SCPClient
import os

base_dir = "../../../"


deploy_device_ip = "192.168.10.10"
device_username = 'shahid'
device_pass = 'shahid007'


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
    

    append_record_file.write(deploy_device_ip+"\n")


read_record_file.close()
append_record_file.close()

ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command("unzip FIT.zip -d FIT")
exit_code = ssh_stdout.channel.recv_exit_status() # handles async exit error 
# exit_code = ssh_stderr.channel.recv_exit_status() # handles async exit error 


for line in ssh_stdout:
    print(line.strip())
# for line in ssh_stderr:
#     print(line.strip())


scp.put(base_dir + "Application-Code/main_file.py", "FIT/Application-Code/main_file.py")
