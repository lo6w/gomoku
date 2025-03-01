import pickle
import random
import socket
import threading
import time
from typing import Literal, Union

from niuben import Sounds
from ui import Multi_play


def get_time() -> str:
    t = time.localtime()
    return '[' + str(t.tm_hour) + ':' + str(t.tm_min) + ':' + str(t.tm_sec) + ']'


class server:
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    name = ''
    send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    send.settimeout(1)
    stop = False
    describe = '这是一个棋室'
    only_server = True
    player1 = '1'
    player2 = '2'
    player1_address = ()
    player2_address = ()
    steps1 = 0
    steps2 = 0
    board = []
    for i in range(16):
        board.append([0] * 16)
    port = 0
    go = 0
    down = ()
    result = {}
    first = ''
    winner = 0
    win_line = [(0, 0), (0, 0)]
    player1_previous = (0, 0)
    player2_previous = (0, 0)
    restart = False
    history = []
    main = False

    def __init__(self, sounds: Sounds, only_server=False) -> None:
        self.sound = sounds
        self.only_server = only_server
        if not self.only_server:
            print(self.hostname + ':' + self.ip)

    def board_init(self):
        self.board = []
        for i in range(16):
            self.board.append([0] * 16)
        self.steps1 = 0
        self.steps2 = 0
        self.winner = 0
        self.win_line = [(0, 0), (0, 0)]

    def step(self, player: Literal[1, 2]):
        if player == 1:
            self.steps1 = self.steps1 + 1
        else:
            self.steps2 = self.steps2 + 1

    def reset(self):
        self.board = []
        for i in range(16):
            self.board.append([0] * 16)
        self.go = 0
        self.player2_address = ()
        self.player2 = ''
        self.first = ''
        self.steps1 = 0
        self.steps2 = 0
        self.winner = 0
        self.win_line = [(0, 0), (0, 0)]

    def judgment(self) -> None:
        if (self.steps1 + self.steps2) <= 256:
            for x in range(16):
                for y in range(16):
                    for x_add in range(3):
                        x_add = x_add - 1
                        for y_add in range(3):
                            y_add = y_add - 1
                            if not (x_add == 0 and y_add == 0) and self.winner == 0:
                                line = [0, 0, 0, 0, 0]
                                for long in range(5):
                                    c = self.read(x + long * x_add, y + long * y_add)
                                    if c is not None:
                                        if c != 0:
                                            line[long] = c
                                        else:
                                            break
                                    else:
                                        break
                                if line == [1, 1, 1, 1, 1]:
                                    self.winner = 1
                                elif line == [2, 2, 2, 2, 2]:
                                    self.winner = 2
                                if self.winner != 0:
                                    self.win_line = [(x, y), (x + 4 * x_add, y + 4 * y_add)]
        else:
            self.winner = 3

    def read(self, x, y) -> Union[int, None]:
        """读取棋盘"""
        if x >= 16 or x < 0 or y >= 16 or y < 0:
            return None
        else:
            return self.board[y][x]

    def add_history(self, text):
        self.history.append((time.time(), str(text)))
        if not self.main:
            self.send.sendto(pickle.dumps({'type': 'msg', 'msg': text}), self.player1_address)

    def getter(self):
        while not self.stop:
            try:
                i = self.send.recvfrom(65536)
                info = pickle.loads(i[0])
                if isinstance(info, dict) and len(info) > 0:
                    info: dict
                    if info['type'] == 'get':
                        if self.go == 0 or self.player2_address == i[1]:
                            self.send.sendto(pickle.dumps({'type': 'info', 'description': self.describe}), i[1])
                        else:
                            self.send.sendto(pickle.dumps({'type': 'full', 'description': self.describe}), i[1])
                    elif info['type'] == 'stop':
                        self.stop = True
                    elif info['type'] == 'exit':
                        print(get_time() + self.player2 + 'has exited')
                        self.add_history(self.player2 + '离开了棋局')
                        self.reset()
                    elif info['type'] == 'join':
                        if self.go == 0 or self.player2_address == i[1]:
                            self.reset()
                            self.player2 = info['name']
                            self.add_history(self.player2 + '加入了棋局')
                            print(get_time() + info['name'] + 'has joined')
                            self.go = random.randint(1, 2)
                            if self.go == 1:
                                self.first = self.player1
                            else:
                                self.first = self.player2
                            self.player2_address = i[1]
                            self.player1_address = (self.ip, self.port)
                            self.send.sendto(
                                pickle.dumps({'type': 'go', 'in': True, 'go': self.go, 'player1': self.player1, 'first': self.first}), i[1])
                        else:
                            self.send.sendto(pickle.dumps({'type': 'go', 'in': False, 'go': self.go}), i[1])
                    elif info['type'] == 'ask_rs':
                        self.history.append((time.time(), self.player2 + '请求重新开始'))
                    elif info['type'] == 'msg':
                        self.history.append((time.time(), info['msg']))
                    elif info['type'] == 'say':
                        if info['say'] == 1:
                            if random.randint(0, 1) == 1:
                                self.sound.play('xun1')
                            else:
                                self.sound.play('xun2')
                        if info['say'] == 2:
                            if random.randint(0, 1) == 1:
                                self.sound.play('ngm1')
                            else:
                                self.sound.play('ngm2')
                        if info['say'] == 3:
                            if random.randint(0, 1) == 1:
                                self.sound.play('lblh1')
                            else:
                                self.sound.play('lblh2')
                    elif info['type'] == 'down':
                        self.board[info['y']][info['x']] = 2
                        self.go = 1
                        self.player2_previous = (info['x'], info['y'])
                        self.step(2)
                        self.judgment()
                    else:
                        if self.only_server:
                            print(get_time() + '未知1:' + str(info))
                else:
                    if self.only_server:
                        print(get_time() + '未知2:' + str(info))
            except socket.timeout:
                if self.go != 0:
                    try:
                        self.send.sendto(pickle.dumps({'type': 'test'}), self.player2_address)
                    except Exception as ep:
                        self.go = 0
                        if self.only_server:
                            print(get_time() + str(ep))
                        self.player2_address = ()
                time.sleep(0.05)
            except ConnectionResetError:
                self.reset()

    def sends(self, x: int, y: int, m: Multi_play):
        if m.main:
            self.send.sendto(pickle.dumps({'type': 'down', 'x': x, 'y': y, 'steps1': self.steps1, 'steps2': self.steps2}),
                             self.player2_address)
            self.step(1)
            self.go = 2
        else:
            self.send.sendto(pickle.dumps({'type': 'down', 'x': x, 'y': y, 'steps1': self.steps1, 'steps2': self.steps2}),
                             self.player1_address)
            self.step(2)
            self.go = 1
        self.judgment()

    def get_date(self):
        while not self.stop:
            try:
                result = pickle.loads(self.send.recv(4096))
                if result['type'] == 'stop':
                    break
                elif result['type'] == 'down':
                    self.board[result['y']][result['x']] = 1
                    self.step(1)
                    self.go = 2
                    self.steps1 = result['steps1']
                    self.steps2 = result['steps2']
                elif result['type'] == 'won':
                    self.winner = result['winner']
                    if self.winner != 3:
                        self.win_line = result['win_line']
                    self.board[result['y']][result['x']] = 1
                    self.go = 3
                    self.steps1 = result['steps1']
                    self.steps2 = result['steps2']
                elif result['type'] == 'msg':
                    self.history.append((time.time(), result['msg']))
                elif result['type'] == 'rs_y':
                    self.go = result['go']
                    self.board_init()
            except ConnectionResetError:
                break
            except KeyError as ke:
                print(get_time() + str(ke) + ' not found')
            except socket.timeout:
                time.sleep(0.1)

    def sender(self):
        while not self.stop:
            time.sleep(0.1)
            if self.winner != 0 and self.go != 3:
                if self.winner == 1:
                    self.send.sendto(
                        pickle.dumps(
                            {'type': 'won', 'win_line': self.win_line, 'go': 1, 'steps1': self.steps1,
                             'x': self.player1_previous[0], 'y': self.player1_previous[1],
                             'steps2': self.steps2, 'winner': self.winner}), self.player2_address)
                    self.add_history(self.player1 + '赢了')
                    self.send.sendto(pickle.dumps({'type': 'msg', 'msg': self.player1 + '赢了'}), self.player2_address)
                    print(get_time() + '2has won')
                    self.go = 3
                elif self.winner == 2:
                    self.send.sendto(
                        pickle.dumps(
                            {'type': 'won', 'win_line': self.win_line, 'go': 2, 'steps1': self.steps1,
                             'x': self.player2_previous[0], 'y': self.player2_previous[1],
                             'steps2': self.steps2, 'winner': self.winner}), self.player2_address)
                    self.add_history(self.player2 + '赢了')
                    self.send.sendto(pickle.dumps({'type': 'msg', 'msg': self.player2 + '赢了'}), self.player2_address)
                    print(get_time() + '2has won')
                    self.go = 3
                else:
                    self.send.sendto(
                        pickle.dumps(
                            {'type': 'won', 'win_line': self.win_line, 'go': 3, 'steps1': self.steps1,
                             'x': self.player2_previous[0], 'y': self.player2_previous[1],
                             'steps2': self.steps2, 'winner': self.winner}), self.player2_address)
                    self.add_history('平局')
                    self.send.sendto(pickle.dumps({'type': 'msg', 'msg': '平局'}), self.player2_address)
                    print(get_time() + 'no one won')
                    self.go = 3

    thread1 = threading.Thread(target=getter, daemon=True)
    thread2 = threading.Thread(target=sender, daemon=True)
    thread3 = threading.Thread(target=get_date, daemon=True)

    def ask_information(self, address):
        self.send.sendto(pickle.dumps({'type': 'get'}), address)
        try:
            g = self.send.recvfrom(4096)
            if g[1] == address:
                self.result = pickle.loads(g[0])
            else:
                self.result = {}
        except ConnectionResetError as cr:
            if self.only_server:
                print(cr)
            self.result = {}
        except socket.timeout:
            self.result = {}

    def get_information(self, address) -> dict:
        self.result = {}
        thread_get = threading.Thread(target=self.ask_information, daemon=True, args=(address,))
        thread_get.start()
        thread_get.join(0.2)
        if thread_get.is_alive():
            return {}
        else:
            return self.result

    def send_exit_message(self) -> None:
        self.send.sendto(pickle.dumps({'type': 'exit'}), self.player2_address)

    def send_restart_message(self) -> None:
        self.send.sendto(pickle.dumps({'type': 'ask_rs'}), self.player2_address)
        self.history.append((time.time(), self.player2 + '请求重新开始'))

    def start_server(self, port: int):
        self.port = port
        self.send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.send.bind((self.ip, self.port))
        print(get_time() + '在' + str(self.port) + '端口上开启服务器')
        self.thread1 = threading.Thread(target=self.getter, daemon=True)
        self.thread1.start()
        self.thread2 = threading.Thread(target=self.sender, daemon=True)
        self.thread2.start()

    def run(self, port: int):
        self.port = port
        self.send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.send.bind((self.ip, self.port))
        print(get_time() + '在' + str(self.port) + '端口上开启服务器')
        self.thread1 = threading.Thread(target=self.getter, daemon=True)
        self.thread1.start()
        while not self.stop:
            time.sleep(0.1)
            if self.go != 0:
                if self.winner == 0:
                    self.judgment()
                elif self.winner == 1:
                    self.send.sendto(
                        pickle.dumps(
                            {'type': 'won', 'win_line': self.win_line, 'go': 1, 'steps1': self.steps1,
                             'x': self.player1_previous[0], 'y': self.player1_previous[1],
                             'steps2': self.steps2, 'winner': self.winner}), self.player2_address)
                    print(get_time() + '2has won')
                    self.go = 3
                else:
                    self.send.sendto(
                        pickle.dumps(
                            {'type': 'won', 'win_line': self.win_line, 'go': 2, 'steps1': self.steps1,
                             'x': self.player2_previous[0], 'y': self.player2_previous[1],
                             'steps2': self.steps2, 'winner': self.winner}), self.player2_address)
                    print(get_time() + '2has won')
                    self.go = 3

    def send_join(self, address):
        self.send.sendto(pickle.dumps({'type': 'join', 'name': self.player2}), address)
        try:
            self.result = pickle.loads(self.send.recvfrom(4096)[0])
            if self.result['type'] == 'go':
                if self.result['in']:
                    self.go = self.result['go']
                else:
                    self.go = 0
        except socket.timeout:
            self.go = 0

    def join(self, address, player2_name: str) -> bool:
        self.player2 = player2_name
        self.result = {}
        self.send.connect(address)
        self.player1_address = address
        self.send.sendto(pickle.dumps({'type': 'join', 'name': self.player2}), address)
        try:
            self.result = pickle.loads(self.send.recvfrom(4096)[0])
            if self.result['type'] == 'go':
                if self.result['in']:
                    self.player1 = self.result['player1']
                    self.go = self.result['go']
                    self.first = self.result['first']
                    self.send.connect(address)
                    self.thread3 = threading.Thread(name='get', target=self.get_date, daemon=True)
                    self.thread3.start()
                    return True
                else:
                    self.go = 0
                    return False
        except socket.timeout:
            self.go = 0
            return False
