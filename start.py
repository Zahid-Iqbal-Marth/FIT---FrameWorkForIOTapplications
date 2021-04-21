from subprocess import call
import threading



def run_back_end():
    call(["./Back-end/FIT/back-end.sh"])

def run_front_end():
    call(["./Front-end/FIT-GUI/front-end.sh"])

def run_zookeeper():
    call(["./kafka/run_zookeeper.sh"])

def run_kafka():
    call(["./kafka/run_kafka.sh"])



a = threading.Thread(target=run_back_end,)
a.start()

b = threading.Thread(target=run_front_end, )
b.start()

c = threading.Thread(target=run_zookeeper, )
c.start()

d = threading.Thread(target=run_kafka, )
d.start()