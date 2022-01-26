# main 실행 파일
# 사용자에게서 입력값을 받아 자료구조를 만들고
# 그것을 토대로 각 노드 별 소켓을 만들어서 할당해준다.
import multiprocessing
import os

import middle_node
import leaf_node
import root_node
import queue
import sys
import time
import configparser
import socket

start_time = time.time()  # 프로그램을 실행한지 시간이 얼마나 지났는지 알려주기 위한 시작 시간
num_of_child = []  # 각 노드의 자식 수
child_node = []  # 각 노드의 자식 노드들의 index
parent_node = []  # 각 노드의 부모 노드의 index
is_leaf = []  # 각 노드가 말단 노드인지 확인해주는 배열. 0 혹은 1이 있다.
sparse_matrix = []  # 노드 별 연결 관계를 나타내느 sparse matrix
N, R = -1, 1  # 총 노드 개수, 루트 노드 번호.
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def make_leaf_node(self_adr, parent_adr):
    leaf_node.leaf_node(self_adr, parent_adr)


def make_middle_node(self_adr, child_num, parent_adr, mid_node_op, mid_node_print, mid_node_interval):
    middle_node.middle_node(self_adr, child_num, parent_adr, mid_node_op, mid_node_print, mid_node_interval)


def make_root_node(self_adr, child_num):
    root_node.root_node(self_adr, child_num)


# 입력받은 edges 정보를 가지고 각 노드별 자식노드의 수, 자식노드의 번호, 부모노드, 리프 노드 유무 값을 넣어준다.
def define_node_attributes(index, parent):
    global num_of_child, child_node, parent_node, is_leaf
    parent_node[index] = parent
    ind_to_pop = -1
    for ind, node in enumerate(child_node[index]):
        if node == parent:
            ind_to_pop = ind
            continue
        define_node_attributes(node, index)
    if ind_to_pop != -1:
        child_node[index].pop(ind_to_pop)
        if num_of_child[index] == 0:
            is_leaf[index] = 1


# leaf node 가 보내는 data 의 range 를 재정의 해주는 함수다. 이걸 설정하기 전 leaf node 의 기본 값은 무조건 1만 보내게 되어있다.
def change_leaf_node_data_range(new_op):
    if len(new_op) != 3 or not new_op[1].isnumeric() or not new_op[2].isnumeric() or int(new_op[1]) >= int(new_op[2]):
        print("Not proper argument for '{}' command".format(*new_op))
        return
    new_op[1] = int(new_op[1])
    new_op[2] = int(new_op[2])
    for i in range(1, N + 1):
        if is_leaf[i] == 1 and i != R:
            sock.sendto(str(new_op).encode('utf-8'), ('127.0.0.1', 10000 + i))


# leaf node 가 데이터를 보내는 주기를 바꿔준다.
def change_leaf_node_interval(new_op):
    if len(new_op) != 2 or not new_op[1].isnumeric():
        print("Not proper argument for '{}' command".format(*new_op))
        return
    new_op[1] = int(new_op[1])
    for i in range(1, N + 1):
        if is_leaf[i] == 1 and i != R:
            sock.sendto(str(new_op).encode('utf-8'), ('127.0.0.1', 10000 + i))


# mid node 가 수행하는 operation 을 바꾸어준다.
def change_mid_node_op(new_op):
    if len(new_op) != 2 or new_op[1] != "max" and new_op[1] != "average" and new_op[1] != "pass":
        print("Not proper argument for '{}' command".format(*new_op))
        return
    for i in range(1, N + 1):
        if is_leaf[i] == 0 and i != R:
            sock.sendto(str(new_op).encode('utf-8'), ('127.0.0.1', 10000 + i))


# mid node 가 데이터를 보내는 주기를 바꾸어준다.
def change_mid_node_interval(new_op):
    if len(new_op) != 2 or not new_op[1].isnumeric():
        print("Not proper argument for '{}' command".format(*new_op))
        return
    new_op[1] = int(new_op[1])
    for i in range(1, N + 1):
        if is_leaf[i] == 0 and i != R:
            sock.sendto(str(new_op).encode('utf-8'), ('127.0.0.1', 10000 + i))


def main():
    global num_of_child, N, R, sparse_matrix, child_node, parent_node, is_leaf

    # config 로 설정 파일 안에 있는 값들을 가져온다.
    config = configparser.ConfigParser()
    config.read(sys.argv[1], encoding='UTF8')
    mid_node_op = config.get("config", "mid_node_op")
    mid_node_print = eval(config.get("config", "mid_node_print"))
    mid_node_interval = int(config.get("config", "mid_node_interval"))
    input_form = int(config.get("config", "input_form"))  # 입력 형식. 1이면 edges 정보가 있는 파일을 열고, 2이면 차수만 받는다.
    N = int(config.get("tree_info", "node_num"))  # 총 노드 개수

    # 파이썬 자료구조는 자동으로 0번부터 시작하기에, 모든 자료구조는 N+1까지 만들어 준다. (즉 0번 index 의 값은 쓰이지 않는다.)
    parent_node = [0] * (N + 1)
    is_leaf = [0] * (N + 1)
    child_node = [[] for _ in range((N + 1))]

    # edges 정보를 다 입력 받을 경우
    if input_form == 1:
        R = int(config.get("tree_info", "root_index"))  # 루트 노드 index (1부터 시작)
        f = open(config.get("config", "iot_tree_structure_file"), "r", encoding='UTF8')
        num_of_child = [-1] * (N + 1)
        num_of_child[R] += 1
        for i in range(N - 1):
            tmp_node1, tmp_node2 = [int(x) for x in f.readline().split()]
            num_of_child[tmp_node1] += 1
            num_of_child[tmp_node2] += 1
            child_node[tmp_node1].append(tmp_node2)
            child_node[tmp_node2].append(tmp_node1)

        # 사용자가 입력한 edges 정보를 가지고 자식 노드의 수, 부모 노드의 번호 등을 define_node_attributes 함수 안에서 지정해 준다.
        # 첫 번째 인자에는 노드 번호, 두 번째 인자에는 해당 노드의 부모의 번호를 넘겨준다. 루트 노드는 부모 노드가 없기에 두번째 인자가 -1이다.
        define_node_attributes(R, -1)

    # 차수를 가지고 자동으로 생성할 경우
    elif input_form == 2:
        fan_out_degree = int(config.get("tree_info", "fan_out_degree"))  # 차수
        num_of_child = [0] * (N + 1)
        cur_ind = 1
        # complete 트리를 1번 노드를 루트로 하게 만들어 준다.
        for i in range(2, N + 1):
            if num_of_child[cur_ind] >= fan_out_degree:
                cur_ind += 1
            num_of_child[cur_ind] += 1
            child_node[cur_ind].append(i)
            parent_node[i] = cur_ind
        for i in range(1, N + 1):
            if num_of_child[i] == 0:
                is_leaf[i] = 1

    else:
        print("올바르지 않은 입력 형식입니다.")
        exit(1)

    # 루트 노드부터 BFS 로 하나하나 소켓을 지정해준다.
    pool = multiprocessing.Pool(processes=N)
    pool.apply_async(make_root_node, [10000 + R, num_of_child[R]])
    q = queue.Queue()
    q.put(R)
    while not q.empty():
        node_num = q.get()
        for i in child_node[node_num]:
            if is_leaf[i] == 1:
                pool.apply_async(make_leaf_node, [10000 + i, 10000 + node_num])
            else:
                pool.apply_async(make_middle_node,
                                 [10000 + i, num_of_child[i], 10000 + node_num, mid_node_op, mid_node_print,
                                  mid_node_interval])
                q.put(i)

    # 보기 편하도록 매 초마다 running time 을 찍어준다.
    # while True:
    #     if (time.time() - start_time) % 1 < 0.01:
    #         print(int(time.time() - start_time), "초:")
    #         time.sleep(0.1)
    os.system('python app.py')
    # operations 안에는 실행할 수 있는 모든 operations 들이 있고, console 은 shell 처럼 명령어를 기다린다.
    operations = {"chmidop": change_mid_node_op, "chmidintvl": change_mid_node_interval,
                  "chleafdata": change_leaf_node_data_range, "chleafintvl": change_leaf_node_interval}
    while True:
        # 사용자가 실행할 수 있는 operation 명을 입력했다면, 해당 operation 을 실행할 수 있는 함수를 호출해준다.
        command = [x for x in input().split()]
        if len(command) > 0 and command[0] in operations:
            operations[command[0]](command)
        elif len(command) == 0:
            continue
        else:
            print("'{}' not found. Type help for a list of commands".format(*command))


if __name__ == "__main__":
    main()
