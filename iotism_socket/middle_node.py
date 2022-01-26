# 중간 노드들로써, 자식에게서 받은 데이터를 저장하고 있다가, 사용자가 지정한 interval 마다 데이터를 부모에게 보내준다.

import socket
import threading
import time
from ast import literal_eval

self_adr, mid_node_op, parent_adr, child_num, mid_node_print, mid_node_interval = 0, 0, 0, 0, 0, 0
existed = {}  # 자식에게서 받은 데이터를 보관하는 dict
sock = socket.socket()
received_child_cnt = 0  # 데이터를 현재 노드에게 넘겨준 자식의 수


# mid_node_interval 마다 값을 보내줘야하기에, threading 으로 해당 초만큼 sleep 후 값을 보내주는 operation 함수 호출
# operation 함수 내에서 다시 thread 를 호출해 주기에, interval 처럼 작동하게 된다.
class SendData(threading.Thread):
    def __init__(self, sec):
        super().__init__()
        self.sec = sec  # thread 이름 지정

    def run(self):
        time.sleep(self.sec)
        operation_and_send()


# 자식으로부터 받은 값을 그대로 보낸다.
def pass_data(data_to_send):
    sock.sendto(str(data_to_send).encode('utf-8'), ('127.0.0.1', parent_adr))
    # 데이터를 몇번 노드에 보내주었는지 출력해준다.
    if mid_node_print:
        print("노드 {}: send {} to {}".format(self_adr, data_to_send, parent_adr))


# 자식으로부터 받은 값들의 평균을 보낸다.
def pass_average_data(data_to_send):
    sock.sendto(str([sum(data_to_send) / received_child_cnt]).encode('utf-8'), ('127.0.0.1', parent_adr))
    # 데이터를 몇번 노드에 보내주었는지 출력해준다.
    if mid_node_print:
        print("노드 {}: send {} to {}".format(self_adr, [sum(data_to_send) / received_child_cnt], parent_adr))


# 자식으로부터 받은 값들 중 최대 값을 보낸다.
def pass_max_data(data_to_send):
    sock.sendto(str([max(data_to_send)]).encode('utf-8'), ('127.0.0.1', parent_adr))
    # 데이터를 몇번 노드에 보내주었는지 출력해준다.
    if mid_node_print:
        print("노드 {}: send {} to {}".format(self_adr, [max(data_to_send)], parent_adr))


# 지금까지 자식에게서 받은 데이터를 모아다가 명령어 코드에 따라 해당 계산을 실행한 뒤, 데이터를 부모에게 보내주는 함수.
def operation_and_send():
    global received_child_cnt, existed
    merged_data = []  # 받은 데이터들을 배열 형태로 하나로 합침
    for lists in existed.values():
        for i in lists:
            merged_data.append(i)
    if len(merged_data) == 0:
        if mid_node_print:
            print("노드 {}: 보낼 데이터가 하나도 없습니다.".format(self_adr))
        thread_send = SendData(mid_node_interval)
        thread_send.start()
        return
    if mid_node_op == "pass":
        pass_data(merged_data)
    elif mid_node_op == "average":
        pass_average_data(merged_data)
    elif mid_node_op == "max":
        pass_max_data(merged_data)
    # 데이터를 현재 노드에게 넘겨준 자식의 수 및 데이터 저장하는 dict 를 초기화 후 다시 thread 를 호출해준다.
    received_child_cnt = 0
    existed = {}
    thread_send = SendData(mid_node_interval)
    thread_send.start()


def middle_node(adr, child_num_received, parent_adr_received, mid_node_op_received, mid_node_print_received,
                mid_node_interval_received):
    global sock, self_adr, existed, mid_node_op, parent_adr, child_num, mid_node_print, mid_node_interval, \
        received_child_cnt
    self_adr = adr
    child_num = child_num_received  # 자식의 수
    parent_adr = parent_adr_received  # 부모 노드의 주소
    mid_node_op = mid_node_op_received  # 해당 노드에서 할 계산 종류를 정하는 변수 (pass/average/max)
    mid_node_print = mid_node_print_received  # 해당 노드에서 데이터를 보낼 때 그 값을 출력 할 것인지 (boolean)
    mid_node_interval = mid_node_interval_received  # 해당 노드에서 몇 초 주기로 데이터를 부모에게 올려줄 것인지 (int)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('127.0.0.1', self_adr))
    # 인터벌 뒤에 데이터를 가공하고 보내주는 operation_and_send 함수를 호출하도록 thread 를 호출해준다.
    thread_send = SendData(mid_node_interval)
    thread_send.start()
    while True:
        dummy, adr1 = sock.recvfrom(1024)
        data = literal_eval(dummy.decode('utf-8'))
        # 만약 이 소켓으로 해당 노드의 operation 을 바꾸거나 interval 을 바꾸라는 명령어가 보내졌다면, 바로 바꿔준다.
        if data[0]=="chmidop":
            mid_node_op=data[1]
        elif data[0]=="chmidintvl":
            mid_node_interval=data[1]
        # 그게 아니라면 자식 노드에서 온 데이터이므로 저장해준다.
        elif adr1 not in existed:
            existed[adr1] = data
            received_child_cnt += 1
        else:
            existed[adr1] = data
