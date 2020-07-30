"""
    author: wang heyu

    To-do:
        1. Test and debug
        2. Format printing
        3. Multiple files
        4. Comments
"""
import time
from random import gauss,random

# 随机函数-时间间隔：根据题目设置为 1 + gauss(0, 0.01)
def rand_t():
    return 1 + gauss(0, 0.01)

# 随机函数-丢包概率：返回值为True时不发生丢包；此处设置为20%丢包率
def rand_l():
    return random() < 0.8

class Packet:
    """Packet类
    
    Packet类: 模拟数据包; 存储序列号, 数据值, 发送者等信息

    Attributes:
        serial_num: Integer, 序列号; 该模拟系统中, 各发送节点序列号由0开始排列
        data: 承载数据; 可改变数据类型
        src: 来源/发送者信息; 可根据需要设置为发送者ID或发送者对象实例
    """
    def __init__(self, serial_num, data, src):
        self.serial_num = serial_num
        self.data = data
        self.src = src

class Sender:
    """Sender类
    
    Sender类: 模拟发送者节点

    Attributes:
        id: String, 发送者id
        receiver: Object, 接收者对象实例
        data: List, 发送数据数组
        rand_t: Function, 时间间隔随机函数
        rand_l: Function, 丢包概率随机函数; 该函数返回True的概率为成功发送(不丢包)的概率
        delay*: Float, 起始滞后时间; 默认值0
        cnt: Integer, 发送次数计数; 同时作为正常依次发送数据时data数组的指针
        msg_sink: List, 重新发送请求列表; 接收Receiver检测到丢包后发送的重新发送请求, 存储方式为数据的对应index
    """
    def __init__(self, id, receiver, data, rand_t, rand_l, delay=0):
        self.id = id
        self.receiver = receiver
        self.data = data
        self.rand_t = rand_t
        self.rand_l = rand_l
        self.time = delay
        self.cnt = 0
        self.msg_sink = []

    def awake(self):
        if len(self.msg_sink) > 0:
            for msg in self.msg_sink:
                packet = Packet(msg, self.data[msg], self)
                self.send(packet, resend=True)
            self.msg_sink = []

        packet = Packet(self.cnt, self.data[self.cnt], self)
        self.send(packet)
        self.cnt += 1
        self.sleep()

    def send(self, packet, resend=False):
        if rand_l():
            self.receiver.put(packet)
        else:
            if resend:
                print('[ INFO ] Packet loss occurred! | id:%3s | serial_num:%3d | resend= True' % (self.id, packet.serial_num))
            else:
                print('[ INFO ] Packet loss occurred! | id:%3s | serial_num:%3d | resend=False' % (self.id, packet.serial_num))

    def sleep(self):
        self.time += self.rand_t()

    def get_loss_msg(self, serial_num):
        self.msg_sink.append(serial_num)
        print('[ INFO ] Loss message received | id:%3s | serial_num:%3d' % (self.id, serial_num))


class Receiver:
    """Receiver类
    
    Receiver类: 模拟接收者节点

    Attributes:
        id: String, 接收者id
        size: Integer, 各发送者的数据存储空间, 即数组的长度
        rand_t: Function, 时间间隔随机函数
        delay*: Float, 起始滞后时间; 默认值0
        cnt: Integer, 输出结果数据计数; 在该系统中, 即已成功求和的数值的计数
        data_sink: Dict:List, 存储来自不同发送者的数据, key值为发送者id; 数据以List存储 
        data_ptr: Dict:Integer, 丢包校检指针, key值为发送者id; 指针数之前的的数据为校检通过(无丢包情况)
        data_cnt: Dict:Integer, 数据接收计数, key值为发送者id; 存储各发送者已成功接收的数据的计数 
        address: Dict:Object, 已对象类型存储发送者地址, key值为发送者id
        output: List, 最终输出结果
    """
    def __init__(self, id, size, rand_t, delay=0):
        self.id = id
        self.size = size
        self.rand_t = rand_t
        self.time = delay
        self.cnt = 0
        self.data_sink = {}
        self.data_ptr = {}
        self.data_cnt = {}
        self.address = {}
        self.output = [-1] * size

    def register(self, sender):
        self.data_sink[sender.id] = [-1] * self.size
        self.data_ptr[sender.id] = 0
        self.data_cnt[sender.id] = 0
        self.address[sender.id] = sender

    def put(self, packet):
        p_src = packet.src.id
        p_serial = packet.serial_num
        p_data = packet.data
        self.data_sink[p_src][p_serial] = p_data
        self.data_cnt[p_src] = max(p_serial+1, self.data_cnt[p_src])
        print('[ INFO ] Packet received!      | id:%3s | serial_num:%3d | data:%3d' % (p_src, p_serial, p_data))

    def awake(self):
        self.check_loss()
        self.add_data()
        self.sleep()

    def check_loss(self):
        for sender in self.data_sink.keys():
            temp_data = self.data_sink[sender]
            temp_ptr = self.data_ptr[sender]
            temp_cnt = self.data_cnt[sender]
            
            first_hit = True
            for i in range(temp_ptr, temp_cnt):


                if temp_data[i] == -1:
                    self.address[sender].get_loss_msg(i)
                    if first_hit:
                        self.data_ptr[sender] = i
                        first_hit = False

            if first_hit == True:
                temp_ptr = temp_cnt
                self.data_ptr[sender] = temp_cnt

    def add_data(self):
        upp_bound = min(self.data_ptr.values())
        temp_cnt = self.cnt
        for i in range(temp_cnt, upp_bound):
            sum_res = 0
            for sender in self.data_sink:
                sum_res += self.data_sink[sender][i]
            self.output[i] = sum_res
            self.cnt += 1
            print('[ INFO ] New data added!       | data:%3d' % (sum_res))

    def sleep(self):
        self.time += self.rand_t()


def main():
    data = [i for i in range(1, 31)]
    C =Receiver('C', 30, rand_t)
    A = Sender('A', C, data, rand_t, rand_l)
    B = Sender('B', C, data, rand_t, rand_l)

    C.register(A)
    C.register(B)

    A_cnt = 0
    B_cnt = 0
    C_cnt = 0
    while True:
        if A.time <= B.time and A.time <= C.time:
            print('-%5.2fs- Sender awakes         | id:%3s' % (A.time, 'A'))
            A.awake()
            time.sleep(2)
            A_cnt += 1
        elif B.time <= A.time and B.time <= C.time:
            print('-%5.2fs- Sender awakes         | id:%3s' % (B.time, 'B'))
            B.awake()
            time.sleep(2)
            B_cnt += 1
        else:
            print('-%5.2fs- Receiver awakes       | id:%3s' % (C.time, 'C'))
            C.awake()
            time.sleep(2)
            C_cnt += 1
        if A_cnt>=30 or B_cnt>=30 or C_cnt>=30:
            break
    print("The sum of the data received :", C.output)
    print("Sent Number for A :", C.data_sink['A'])
    print("Sent Number for B :", C.data_sink['B'])

if __name__ == '__main__':
	main()
