"""
    - 无规则版本，仅计算最新接受的数据
    - 当接收器醒来时，如果有一方未发送，则记为0
"""

import simpy
from random import gauss

class ThreeNodes:
    def __init__(self, env):
        self.env = env
        self.pc1 = env.process(self.packet_sender1(env))
        self.pc2 = env.process(self.packet_sender2(env))
        self.rc = env.process(self.receiver(env))
        global rec_a
        global rec_b
        rec_a = [0]
        rec_b = [0]

    def packet_sender1(self, env):
        data = [i for i in range(1, 100)]
        i = 0
        while True:
            yield env.timeout(1 + gauss(0, 0.01))
            rec_a[0] = data[i]
            print('[%07.4fs] %8s: Sending value  %3d' % (env.now, 'Sender 1', data[i]))
            i += 1
            
    def packet_sender2(self, env):
        data = [i for i in range(1, 100)]
        i = 0
        while True:
            yield env.timeout(1 + gauss(0, 0.01))
            rec_b[0] = data[i]
            print('[%07.4fs] %8s: Sending value  %3d' % (env.now, 'Sender 2', data[i]))
            i += 1
            
    def receiver(self, env):
        res = []
        cnt = 0
        while True:
            yield env.timeout(1 + gauss(0, 0.01))
            
            res.append(rec_a[0] + rec_b[0])
            rec_a[0] = 0
            rec_b[0] = 0
            cnt += 1
            
            print('[%07.4fs] %8s: New data %3d' % (env.now, 'Receiver', res[cnt-1]))
            
            print('--------------Recorded Data--------------')
            print(res)
        
            
def main():
    env = simpy.Environment()
    tn = ThreeNodes(env)
    env.run(until=50)

if __name__ == '__main__':
    main()