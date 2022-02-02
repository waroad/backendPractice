# 루트 노드로써, 필요한 데이터가 다 올때까지 기다리다가 다 도착하면 FINISH 와 함께 받은 데이터들을 출력하고,
# 다음 데이터를 또 받기 위해 가지고 있는 데이터 dict 를 다시 초기화해준다.
import json
import socket
from ast import literal_eval
import requests


def send_api(body):
    API_HOST = "http://127.0.0.1:5000/"
    url = API_HOST
    body = body
    try:
        headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'Accept': '*/*'}
        requests.post(url, headers=headers, data=json.dumps(body, ensure_ascii=False, indent="\t"))
    except Exception as ex:
        print(ex)


def root_node(self_adr, child_num):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('127.0.0.1', self_adr))
    existed = {}  # 자식에게서 받은 데이터를 보관하는 dict
    received_child_cnt = 0  # 데이터를 넘겨준 자식의 수
    while True:
        dummy, adr1 = sock.recvfrom(1024)
        data = literal_eval(dummy.decode('utf-8'))
        if adr1 not in existed:
            existed[adr1] = data
            received_child_cnt += 1
            # 데이터를 넘겨준 자식의 수가 자식의 개수와 같다면, 즉 필요한 데이터가 다 모였다면
            if received_child_cnt == child_num:
                merged_data = []
                for lists in existed.values():
                    for i in lists:
                        merged_data.append(i)
                send_api({"content":merged_data,"adr":self_adr})
                # print("----:최상단 루트노드 {}, 수신 완료. 데이터: {}----".format(self_adr, merged_data))
                received_child_cnt = 0
                existed = {}
        # 이미 같은 자식이 데이터를 보냈었다면, 최신 값으로 업데이트해준다.
        else:
            existed[adr1] = data
