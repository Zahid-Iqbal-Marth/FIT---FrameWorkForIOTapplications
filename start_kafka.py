from subprocess import call
import threading



def run_zookeeper():
    call(["./kafka/run_zookeeper.sh"])

def run_kafka():
    call(["./kafka/run_kafka.sh"])


c = threading.Thread(target=run_zookeeper, )
c.start()

d = threading.Thread(target=run_kafka, )
d.start()