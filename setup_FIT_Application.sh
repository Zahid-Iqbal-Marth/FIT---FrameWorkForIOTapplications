#! /bin/bash


sudo apt install python3-venv
mkdir PythonVirtualEnv
cd PythonVirtualEnv
python3 -m venv FYP
source FYP/bin/activate


git clone https://github.com/Zahid-Iqbal-Marth/FIT---FrameWorkForIOTapplications.git

sudo apt-get install python3-pip

pip3 install kafka-python
pip3 install numpy
pip3 install pandas
pip3 install pillow
pip3 install django
pip3 install opencv-python
pip3 install djangorestframework
pip3 install django-cors-headers
pip3 install tensorflow==2.3.1
pip3 install keras





sudo apt-get install npm
sudo npm install -g @angular/cli
sudo apt install openjdk-11-jdk


cd FIT---FrameWorkForIOTapplications/Front-end/FIT-GUI
npm install
cd .. && cd ..

python3 start.py
