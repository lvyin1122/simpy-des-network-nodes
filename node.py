import time
from random import gauss,random

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
        time: 时间节点, 随sleep()方法更新
        delay: Float, 起始滞后时间; 默认值0
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

    # 苏醒, 首先在msg_sink中查找是否有重新发送请求并发送对应数据
    # 之后根据cnt正常发送数据
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

    # 发送数据方法, 根据rand_l概率发生丢包
    def send(self, packet, resend=False):
        if self.rand_l():
            self.receiver.put(packet)
        else:
            if resend:
                print('[ INFO ] Packet loss occurred! | id:%3s | serial_num:%3d | resend= True' % (self.id, packet.serial_num))
            else:
                print('[ INFO ] Packet loss occurred! | id:%3s | serial_num:%3d | resend=False' % (self.id, packet.serial_num))

    # 睡眠
    def sleep(self):
        self.time += self.rand_t()

    # 从发送者接收丢包信息存储到msg_sink
    def get_loss_msg(self, serial_num):
        self.msg_sink.append(serial_num)
        print('[ INFO ] Loss message received | id:%3s | serial_num:%3d' % (self.id, serial_num))


class Receiver:
    """Receiver类
    
    Receiver类: 模拟接收者节点
    所有的发送者信息都以字典(Dict)形式储存, 因此可以适配两个以上发送者的情况

    Attributes:
        id: String, 接收者id
        size: Integer, 各发送者的数据存储空间, 即数组的长度
        rand_t: Function, 时间间隔随机函数
        time: 时间节点, 随sleep()方法更新
        delay: Float, 起始滞后时间; 默认值0
        cnt: Integer, 输出结果数据计数; 在该系统中, 即已成功求和的数值的计数
        data_sink: Dict->List, 数据容器, 存储来自不同发送者的数据, key值为发送者id; 数据以List存储 
        data_ptr: Dict->Integer, 丢包校检指针, key值为发送者id; 指针数所指之前的的数据为校检通过(无丢包情况)
        data_cnt: Dict->Integer, 数据接收计数, key值为发送者id; 存储各发送者已成功接收的数据的计数
                随最近接收的packet的serial_num更新
        address: Dict->Object, 已对象类型存储发送者地址, key值为发送者id
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

    # 注册所有发送者, 获取发送者地址, 初始化接收对应发送者的容器及其它组件
    def register(self, sender):
        self.data_sink[sender.id] = [-1] * self.size
        self.data_ptr[sender.id] = 0
        self.data_cnt[sender.id] = 0
        self.address[sender.id] = sender

    # 将成功发送的数据存储到对应容器
    def put(self, packet):
        p_src = packet.src.id
        p_serial = packet.serial_num
        p_data = packet.data
        self.data_sink[p_src][p_serial] = p_data
        self.data_cnt[p_src] = max(p_serial+1, self.data_cnt[p_src])
        print('[ INFO ] Packet received!      | id:%3s | serial_num:%3d | data:%3d' % (p_src, p_serial, p_data))

    # 苏醒, 依次执行检查丢包, 数据求和, 睡眠(更新下次苏醒时间)
    def awake(self):
        self.check_loss()
        self.add_data()
        self.sleep()

    # 检查丢包
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

    # 根据校检通过的数据进行求和
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

    # 睡眠
    def sleep(self):
        self.time += self.rand_t()
