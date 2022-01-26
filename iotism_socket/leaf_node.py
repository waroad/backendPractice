# 부모 노드에게 주기적으로 데이터를 보내준다. 현재는 자신의 노드 번호를 데이터로 보내준다.
import time
import socket
import threading
import random
from ast import literal_eval

interval, parent_adr, self_adr = 1, 0, 0
sock = socket.socket()
data_range = [1, 2]  # 보낼 수 있는 data 의 최솟값, 최댓값-1 이다.


# interval 마다 값을 보내줘야하기에, threading 으로 해당 초만큼 sleep 후 값을 보내주는 operation 함수 호출
# send 함수 내에서 다시 thread 를 호출해 주기에, interval 처럼 작동하게 된다.
class SendData(threading.Thread):
    def __init__(self, sec):
        super().__init__()
        self.sec = sec  # thread 이름 지정

    def run(self):
        time.sleep(self.sec)
        send()


# 이 함수 내에서, 정의 된 range 안의 랜덤 데이터를 부모 노드에게 보내준다.
def send():
    global interval, sock
    data = int(random.random() * (data_range[1] - data_range[0]) + data_range[0])
    sock.sendto(str([data]).encode('utf-8'), ('127.0.0.1', parent_adr))
    # print("노드 {}: send {} to {}".format(self_adr, [data], parent_adr))
    thread_send = SendData(interval)
    thread_send.start()


def leaf_node(self_adr_received, parent_adr_received):
    global interval, sock, parent_adr, self_adr
    self_adr = self_adr_received
    parent_adr = parent_adr_received
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('127.0.0.1', self_adr))
    thread_send = SendData(interval)
    thread_send.start()
    # while 문은 사용자가 입력하는 명령어를 기다린다.
    while True:
        dummy, adr1 = sock.recvfrom(1024)
        op_data = literal_eval(dummy.decode('utf-8'))
        if op_data[0] == "chleafdata":
            data_range[0] = op_data[1]
            data_range[1] = op_data[2]
        elif op_data[0] == "chleafintvl":
            interval = op_data[1]
