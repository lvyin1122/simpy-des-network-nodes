"""
    res: 记录接收器输出结果的数组
    sink_a, sink_b: 存储发送数据
    cnt: 记录receiver成功收录的数据数量
    actual_cnt: 当前实际应输出的数组长度，即sink_a, sink_b中长度的最小值
    
    - 每当receiver被唤醒时，比较cnt和actual_cnt，并做差
    - 得到的差itr即为计算求和所需的iteration次数，据此更新结果数组res

"""

import simpy
from random import gauss

class ThreeNodes:
    def __init__(self, env):
        self.env = env
        self.pc1 = env.process(self.packet_sender1(env))
        self.pc2 = env.process(self.packet_sender2(env))
        self.rc = env.process(self.receiver(env))
        global sink_a
        global sink_b
        sink_a = []
        sink_b = []


    def packet_sender1(self, env):
        data = [i for i in range(1, 100)]
        i = 0
        while True:
            yield env.timeout(1 + gauss(0, 0.01))
            sink_a.append(data[i])
            print('[%07.4fs] %8s: Sending value  %3d' % (env.now, 'Sender 1', data[i]))
            i += 1
            
    def packet_sender2(self, env):
        data = [i for i in range(1, 100)]
        i = 0
        while True:
            yield env.timeout(1 + gauss(0, 0.01))
            sink_b.append(data[i])
            print('[%07.4fs] %8s: Sending value  %3d' % (env.now, 'Sender 2', data[i]))
            i += 1
            
    def receiver(self, env):
        res = []
        cnt = 0
        while True:
            yield env.timeout(1 + gauss(0, 0.01))

            len_a = len(sink_a)
            len_b = len(sink_b)
            actual_cnt = min(len_a, len_b)
            itr = actual_cnt - cnt
            ptr = cnt
            
            if itr <= 0:
                print('[%07.4fs] %8s: No data collected' % (env.now, 'Receiver'))
                continue
                
            
            for i in range(0, itr):
                sum_val = sink_a[ptr] + sink_b[ptr]
                res.append(sum_val)
                ptr += 1
                cnt += 1
                print('[%07.4fs] %8s: New data %3d' % (env.now, 'Receiver', sum_val))
            
            print('--------------Recorded Data--------------')
            print(res)
        
            
def main():
    env = simpy.Environment()
    tn = ThreeNodes(env)
    env.run(until=50)

if __name__ == '__main__':
    main()