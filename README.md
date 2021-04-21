# FIT---FrameWorkForIOTapplications

# User Manual

# Project Overview

FIT is a framework that allows users to create complex IoT applications that involve
stream processing, event processing, and complex event processing.. FIT is a generic
framework aimed to be usable by the diverse users of CEP. A GUI is built upon the
framework for generic as well as specific applications. Our GUI will enable users to use
some components to create the application's pipeline. These components include:

### Sensors
it will provide data in the form of streams from sensors(we will use
Virtual sensors to test our application)
### Operators
which can contain different functionalities such as object
detection Algorithm, fall detection Algorithm, etc.

Input (From one or more sensors or operators)<br>
Output (Single – result of the applied algorithm)

### Alerts
Messages/Triggers/Automated Actions.<br>
    
As a proof of concept we will add different Virtual sensors, operators and alerts that can be
found in old homes. This will enable caretakers to create complex scenarios by using a
simple configurable graphical user interface. It will help them to automate old homes
according to the needs of each individual resident. Our framework will also help users to
deploy and run these scenarios on different remote machines.. <br>


## 1 - How to run the project :<br>

i) ​ Download the setup_FIT_Application.sh and run it, it’ll install all the dependencies and run servers.<br>
### 2 - Open Browser
Visit ​ http://localhost:4200/<br>
Now you can create different pipelines<br>
### 3 -​ ​ How to use Virtual sensors
i) To add heart sensor, enter ​ /dataset/HR/heart_rate_sensor_data.txt​ in ​ IP/File​ field.<br>
ii) To add a gyroscope, enter ​ gyr.txt​ in ​ IP/File​ field.<br>
iii) To add accelerometer, enter ​ acc.txt​ in ​ IP/File​ field.<br>
iii) To add fall detection enter ​ ./sensors/dataset/fall_detection/cs4.mp4 ​ in surveillance
camera sensor’s ​ IP/File ​ field.<br>
### Note : ​ these restrictions will be removed in final product
### 4 - Deploy Code:
i)After making pipeline click on Deploy button<br>
ii) A dialog box will open<br>
iii) Enter “Destination IP” (device on which you want to deploy your code)<br>
iv) Enter “Destination Username” and “Destination Password”<br>
v) Then Click on ADD and your code will be deployed<br>
### 5 - Run Code/Application Pipeline:
i) Open terminal.<br>
ii) Navigate to ​ ./Application-Code.<br>
iii) Run ​ main_file.py ​ which is the main controller class and whose code is generated.<br>
iv) The output will be displayed either on terminal or email(as alert) based on the
configuration you have chosen while making the pipeline.<br>
### 6 - Working Demo
i) https://youtu.be/iaEcUMfQ1-Y


