"""
Created on Mon July 13

@author: lvyin
"""
import simpy
from random import gauss

class ThreeNodes:
    def __init__(self, env):
        self.env = env
        self.pc1 = env.process(self.packet_sender1(env))
        self.pc2 = env.process(self.packet_sender2(env))
        self.rc = env.process(self.receiver(env))
        self.p1_sent = env.event()
        self.p2_sent = env.event()

    def packet_sender1(self, env):
        data = [i for i in range(1, 100)]
        i = 0
        while True:
            yield env.timeout(1 + gauss(0, 0.01))
            print('[%07.4fs] %8s: Sending value  %3d' % (env.now, 'Sender 1', data[i]))
            self.p1_sent.succeed(data[i])
            i += 1
            
    def packet_sender2(self, env):
        data = [i for i in range(1, 100)]
        i = 0
        while True:
            yield env.timeout(1 + gauss(0, 0.01))
            print('[%07.4fs] %8s: Sending value  %3d' % (env.now, 'Sender 2', data[i]))
            self.p2_sent.succeed(data[i])
            i += 1
            
    def receiver(self, env):
        res = []
        cnt = 0
        while True:
            print('[%07.4fs] %8s: Sleeping' % (env.now, 'Receiver'))
            
            yield self.p1_sent & self.p2_sent
            res.append(self.p1_sent.value + self.p2_sent.value)
            print('[%07.4fs] %8s: Value received %3d' % (env.now, 'Receiver', res[cnt]))
            
            print('--------------Recorded Data--------------')
            print(res)
            self.p1_sent = env.event()
            self.p2_sent = env.event()
            cnt += 1
        
            
def main():
    env = simpy.Environment()
    tn = ThreeNodes(env)
    env.run(until=50)

if __name__ == '__main__':
    main()