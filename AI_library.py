import random


class nb_AI_1:
    board = []
    self_point = []
    player_point = []
    size = 0
    down_chess = []
    self_max_point = []
    player_max_point = []
    fight = 0.8
    reversal = False
    x = 0
    y = 0
    point1 = {
        (0, 0, 0, 0, 0): 0,
        (2, 0, 0, 0, 0): 0,
        (1, 2, 0, 0, 0): 4,
        (1, 1, 2, 0, 0): 8,
        (1, 0, 0, 0, 0): 32,
        (1, 1, 1, 2, 0): 48,
        (1, 1, 0, 0, 0): 64,
        (1, 1, 1, 0, 0): 96,
        (1, 1, 1, 1, 2): 128,
        (1, 1, 1, 1, 0): 128
    }
    point2 = {
        (0, 0, 0, 0, 0): 0,
        (1, 0, 0, 0, 0): 0,
        (2, 1, 0, 0, 0): 4,
        (2, 2, 1, 0, 0): 8,
        (2, 0, 0, 0, 0): 32,
        (2, 2, 2, 1, 0): 48,
        (2, 2, 0, 0, 0): 64,
        (2, 2, 2, 0, 0): 96,
        (2, 2, 2, 2, 1): 128,
        (2, 2, 2, 2, 0): 128
    }

    def __init__(self, size=16, fight=0.8, reversal=False):
        self.reversal = reversal
        self.fight = fight
        self.size = size
        self.self_point = []
        self.player_point = []
        for i in range(self.size):
            self.self_point.append([0] * self.size)
            self.player_point.append([0] * self.size)

    def read(self, x, y):
        if x >= 16 or x < 0 or y >= 16 or y < 0:
            return None
        else:
            return self.board[y][x]

    def get_point(self, chess=1):
        max_point = 0
        points = []
        for x in range(self.size):
            for y in range(self.size):
                if chess in [self.read(x - 1, y - 1), self.read(x, y - 1), self.read(x + 1, y - 1),
                             self.read(x - 1, y), self.read(x + 1, y),
                             self.read(x - 1, y + 1), self.read(x, y + 1), self.read(x + 1, y + 1)] and self.board[y][
                    x] == 0:
                    for x_add in range(3):
                        x_add = x_add - 1
                        for y_add in range(3):
                            y_add = y_add - 1
                            if not (x_add == 0 and y_add == 0):
                                line = [0, 0, 0, 0, 0]
                                for long in range(5):
                                    c = self.read(x + (long + 1) * x_add, y + (long + 1) * y_add)
                                    if c is not None:
                                        if c != 0:
                                            line[long] = c
                                        else:
                                            break
                                    else:
                                        break
                                f = (line[0], line[1], line[2], line[3], line[4])
                                if chess == 1 and f in self.point1:
                                    self.player_point[y][x] = self.player_point[y][x] + self.point1[f]
                                elif chess == 2 and f in self.point2:
                                    self.self_point[y][x] = self.self_point[y][x] + self.point2[f]
                    if chess == 1:
                        if max_point < self.player_point[y][x]:
                            max_point = self.player_point[y][x]
                            points = [[x, y]]
                        elif max_point == self.player_point[y][x]:
                            points.append([x, y])
                    elif chess == 2:
                        if max_point < self.self_point[y][x]:
                            max_point = self.self_point[y][x]
                            points = [[x, y]]
                        elif max_point == self.self_point[y][x]:
                            points.append([x, y])
        if len(points) == 1:
            p = points[0]
        elif len(points) > 1:
            p = points[random.randint(0, len(points) - 1)]
        else:
            p = None
        if chess == 1:
            self.player_max_point = [max_point, p]
        if chess == 2:
            self.self_max_point = [max_point, p]

    def get(self, board: list, reversal=False):
        self.reversal = reversal
        self.board = board
        t = 0
        for x in range(16):
            for y in range(16):
                if self.board[y][x] != 0:
                    t = t + 1
        if t <= 256:
            self.self_point.clear()
            self.player_point.clear()
            for i in range(self.size):
                self.self_point.append([0] * self.size)
                self.player_point.append([0] * self.size)
            self.get_point(1)
            self.get_point(2)
            if self.reversal:
                c = 1
            else:
                c = 2
            if self.self_max_point[1] is None and self.player_max_point[1] is None:
                self.x = random.randint(0, 15)
                self.y = random.randint(0, 15)
            else:
                if self.reversal:
                    if self.player_max_point[0] * self.fight > self.self_max_point[0]:
                        self.x = self.player_max_point[1][0]
                        self.y = self.player_max_point[1][1]
                    else:
                        if not self.self_max_point[1] is None:
                            self.x = self.self_max_point[1][0]
                            self.y = self.self_max_point[1][1]
                else:
                    if self.self_max_point[0] * self.fight > self.player_max_point[0]:
                        self.x = self.self_max_point[1][0]
                        self.y = self.self_max_point[1][1]
                    else:
                        if not self.player_max_point[1] is None:
                            self.x = self.player_max_point[1][0]
                            self.y = self.player_max_point[1][1]
            board[self.y][self.x] = c
            self.get_point(1)
            self.get_point(2)


class nb_AI_2:
    web_broad = 16
    NONE = 0,  # 无
    SLEEP_TWO = 1,  # 眠二
    LIVE_TWO = 2,  # 活二
    SLEEP_THREE = 3,  # 眠三
    LIVE_THREE = 4,  # 活三
    CHONG_FOUR = 5,  # 冲四
    LIVE_FOUR = 6,  # 活四
    LIVE_FIVE = 7,  # 活五

    # 方便后续调用枚举内容
    FIVE = 7
    L4, L3, L2 = 6, 4, 2
    S4, S3, S2 = 5, 3, 1
    x, y = 0, 0

    def __init__(self, chess_len=16):  # 构造函数
        self.save_count = 0
        self.len = chess_len  # 当前棋盘大小
        # 二维数组，每一格存的是：横评分，纵评分，左斜评分，右斜评分
        self.record = [[[0, 0, 0, 0] for _ in range(chess_len)] for _ in range(chess_len)]
        # 存储当前格具体棋型数量
        self.count = [[0 for _ in range(8)] for _ in range(2)]
        # 位置分（同条件下越靠近棋盘中央越高）
        self.position_is_great = [
            [(self.web_broad - max(abs(i - self.web_broad / 2 + 1), abs(j - self.web_broad / 2 + 1))) for i in
             range(chess_len)]
            for j in range(chess_len)]

    def get_init(self):  # 初始化
        for i in range(self.len):
            for j in range(self.len):
                for k in range(4):
                    self.record[i][j][k] = 0
        for i in range(len(self.count)):
            for j in range(len(self.count[0])):
                self.count[i][j] = 0
        self.save_count = 0

    def is_win(self, board, turn):  # 当前人胜利
        return self.evaluate(board, turn, True)

    # 返回所有未下棋坐标（位置从好到坏）
    def gen_move(self, board):
        moves = []
        for y in range(self.len):
            for x in range(self.len):
                if board[y][x] == 0:
                    score = self.position_is_great[y][x]
                    moves.append((score, x, y))
        moves.sort(reverse=True)
        return moves

    # 返回当前最优解下标
    def search(self, board, turn):
        moves = self.gen_move(board)
        best_move = None
        max_score = -99999  # 无穷小
        for score, x, y in moves:
            board[y][x] = turn
            score = self.evaluate(board, turn)
            board[y][x] = 0
            if score > max_score:
                max_score = score
                best_move = (max_score, x, y)
        return best_move

    # 主要用于测试的函数，现在已经没什么用
    def get(self, board: list, turn=2):
        # time1 = time.time()
        score, x, y = self.search(board, turn)
        self.x = x
        self.y = y
        # time2 = time.time()
        # print('time:%f  (%d, %d)' % ((time2 - time1), x, y))
        board[y][x] = turn

    # 得出一点的评分
    # 直接列举所有棋型
    def get_score(self, my_chess, your_chess):
        mscore, oscore = 0, 0
        if my_chess[self.FIVE] > 0:
            return 10000, 0
        if your_chess[self.FIVE] > 0:
            return 0, 10000
        if my_chess[self.S4] >= 2:
            my_chess[self.L4] += 1
        if your_chess[self.L4] > 0:
            return 0, 9050
        if your_chess[self.S4] > 0:
            return 0, 9040
        if my_chess[self.L4] > 0:
            return 9030, 0
        if my_chess[self.S4] > 0 and my_chess[self.L3] > 0:
            return 9020, 0
        if your_chess[self.L3] > 0 and my_chess[self.S4] == 0:
            return 0, 9010
        if my_chess[self.L3] > 1 and your_chess[self.L3] == 0 and your_chess[self.S3] == 0:
            return 9000, 0
        if my_chess[self.S4] > 0:
            mscore += 2000
        if my_chess[self.L3] > 1:
            mscore += 500
        elif my_chess[self.L3] > 0:
            mscore += 100
        if your_chess[self.L3] > 1:
            oscore += 2000
        elif your_chess[self.L3] > 0:
            oscore += 400
        if my_chess[self.S3] > 0:
            mscore += my_chess[self.S3] * 10
        if your_chess[self.S3] > 0:
            oscore += your_chess[self.S3] * 10
        if my_chess[self.L2] > 0:
            mscore += my_chess[self.L2] * 4
        if your_chess[self.L2] > 0:
            oscore += your_chess[self.L2] * 4
        if my_chess[self.S2] > 0:
            mscore += my_chess[self.S2] * 4
        if your_chess[self.S2] > 0:
            oscore += your_chess[self.S2] * 4
        return mscore, oscore  # 自我辅助效果，counter对面效果

    # 对上述得分进行进一步处理
    def evaluate(self, board, turn, check_win=False):
        self.get_init()
        if turn == 1:
            me = 1
            you = 2
        else:
            me = 2
            you = 1
        for y in range(self.len):
            for x in range(self.len):
                if board[y][x] == me:
                    self.evaluatePoint(board, x, y, me, you)
                elif board[y][x] == you:
                    self.evaluatePoint(board, x, y, you, me)
        my_chess = self.count[me - 1]
        your_chess = self.count[you - 1]
        if check_win:
            return my_chess[self.FIVE] > 0  # 检查是否已经胜利
        else:
            mscore, oscore = self.get_score(my_chess, your_chess)
            return mscore - oscore  # 自我辅助效果，counter对面效果

    def evaluatePoint(self, board, x, y, me, you):
        direction = [(1, 0), (0, 1), (1, 1), (1, -1)]  # 四个方向
        for i in range(4):
            if self.record[y][x][i] == 0:
                # 检查当前方向棋型
                self.getBasicSituation(board, x, y, i, direction[i], me, you, self.count[me - 1])
            else:
                self.save_count += 1

    # 把当前方向棋型存储下来，方便后续使用
    def getLine(self, board, x, y, direction, me, you):
        line = [0 for i in range(9)]
        # “光标”移到最左端
        tmp_x = x + (-5 * direction[0])
        tmp_y = y + (-5 * direction[1])
        for i in range(9):
            tmp_x += direction[0]
            tmp_y += direction[1]
            if tmp_x < 0 or tmp_x >= self.len or tmp_y < 0 or tmp_y >= self.len:
                line[i] = you  # 出界
            else:
                line[i] = board[tmp_y][tmp_x]
        return line

    # 把当前方向的棋型识别成具体情况（如把MMMMX识别成冲四）
    def getBasicSituation(self, board, x, y, dir_index, dir, me, you, count):
        # record赋值
        def setRecord(self, x, y, left, right, dir_index, direction):
            tmp_x = x + (-5 + left) * direction[0]
            tmp_y = y + (-5 + left) * direction[1]
            for i in range(left, right):
                tmp_x += direction[0]
                tmp_y += direction[1]
                self.record[tmp_y][tmp_x][dir_index] = 1

        empty = 0
        left_index, right_index = 4, 4
        line = self.getLine(board, x, y, dir, me, you)
        while right_index < 8:
            if line[right_index + 1] != me:
                break
            right_index += 1
        while left_index > 0:
            if line[left_index - 1] != me:
                break
            left_index -= 1
        left_range, right_range = left_index, right_index
        while right_range < 8:
            if line[right_range + 1] == you:
                break
            right_range += 1
        while left_range > 0:
            if line[left_range - 1] == you:
                break
            left_range -= 1
        chess_range = right_range - left_range + 1
        if chess_range < 5:
            setRecord(self, x, y, left_range, right_range, dir_index, dir)
            return self.NONE
        setRecord(self, x, y, left_index, right_index, dir_index, dir)
        m_range = right_index - left_index + 1
        if m_range == 5:
            count[self.FIVE] += 1
        # 活四冲四
        if m_range == 4:
            left_empty = right_empty = False
            if line[left_index - 1] == empty:
                left_empty = True
            if line[right_index + 1] == empty:
                right_empty = True
            if left_empty and right_empty:
                count[self.L4] += 1
            elif left_empty or right_empty:
                count[self.S4] += 1
        # 活三眠三
        if m_range == 3:
            left_empty = right_empty = False
            left_four = right_four = False
            if line[left_index - 1] == empty:
                if line[left_index - 2] == me:  # MXMMM
                    setRecord(self, x, y, left_index - 2, left_index - 1, dir_index, dir)
                    count[self.S4] += 1
                    left_four = True
                left_empty = True
            if line[right_index + 1] == empty:
                if line[right_index + 2] == me:  # MMMXM
                    setRecord(self, x, y, right_index + 1, right_index + 2, dir_index, dir)
                    count[self.S4] += 1
                    right_four = True
                right_empty = True
            if left_four or right_four:
                pass
            elif left_empty and right_empty:
                if chess_range > 5:  # XMMMXX, XXMMMX
                    count[self.L3] += 1
                else:  # PXMMMXP
                    count[self.S3] += 1
            elif left_empty or right_empty:  # PMMMX, XMMMP
                count[self.S3] += 1
        # 活二眠二
        if m_range == 2:
            left_empty = right_empty = False
            left_three = right_three = False
            if line[left_index - 1] == empty:
                if line[left_index - 2] == me:
                    setRecord(self, x, y, left_index - 2, left_index - 1, dir_index, dir)
                    if line[left_index - 3] == empty:
                        if line[right_index + 1] == empty:  # XMXMMX
                            count[self.L3] += 1
                        else:  # XMXMMP
                            count[self.S3] += 1
                        left_three = True
                    elif line[left_index - 3] == you:  # PMXMMX
                        if line[right_index + 1] == empty:
                            count[self.S3] += 1
                            left_three = True
                left_empty = True
            if line[right_index + 1] == empty:
                if line[right_index + 2] == me:
                    if line[right_index + 3] == me:  # MMXMM
                        setRecord(self, x, y, right_index + 1, right_index + 2, dir_index, dir)
                        count[self.S4] += 1
                        right_three = True
                    elif line[right_index + 3] == empty:
                        # setRecord(self, x, y, right_index+1, right_index+2, dir_index, dir)
                        if left_empty:  # XMMXMX
                            count[self.L3] += 1
                        else:  # PMMXMX
                            count[self.S3] += 1
                        right_three = True
                    elif left_empty:  # XMMXMP
                        count[self.S3] += 1
                        right_three = True
                right_empty = True
            if left_three or right_three:
                pass
            elif left_empty and right_empty:  # XMMX
                count[self.L2] += 1
            elif left_empty or right_empty:  # PMMX, XMMP
                count[self.S2] += 1
        # 特殊活二眠二（有空格
        if m_range == 1:
            left_empty = right_empty = False
            if line[left_index - 1] == empty:
                if line[left_index - 2] == me:
                    if line[left_index - 3] == empty:
                        if line[right_index + 1] == you:  # XMXMP
                            count[self.S2] += 1
                left_empty = True
            if line[right_index + 1] == empty:
                if line[right_index + 2] == me:
                    if line[right_index + 3] == empty:
                        if left_empty:  # XMXMX
                            count[self.L2] += 1
                        else:  # PMXMX
                            count[self.S2] += 1
                elif line[right_index + 2] == empty:
                    if line[right_index + 3] == me and line[right_index + 4] == empty:  # XMXXMX
                        count[self.L2] += 1
        # 以上都不是则为none棋型
        return self.NONE
