# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.8.5

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /django_docker

# Set the working directory to /music_service
WORKDIR /django_docker

# Copy the current directory contents into the container at /music_service
ADD . /django_docker/

# Install any needed packages specified in requirements.txt
RUN  pip3 install kafka-python==2.0.2
RUN  pip3 install numpy
RUN  pip3 install pandas
RUN  pip3 install opencv-python
RUN  pip3 install django
RUN  pip3 install djangorestframework==3.12.2
RUN  pip3 install django-cors-headers==3.7.0
RUN  pip3 install tensorflow==2.3.1
RUN  pip3 install keras
RUN  pip3 install confluent-kafka==1.6.0



