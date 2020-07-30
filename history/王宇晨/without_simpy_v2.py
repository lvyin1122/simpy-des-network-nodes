"""
    author: wang heyu

    To-do:
        1. Test and debug
        2. Format printing
        3. Multiple files
        4. Comments
"""

from random import gauss,random

def rand_t():
    return 1 + gauss(0, 0.01)

def rand_l():
    return random() < 1

class Packet:
    """
    

    """
    def __init__(self, serial_num, data, src):
        self.serial_num = serial_num
        self.data = data
        self.src = src

class Sender:
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
                self.receiver.put(packet, resend=True)
            msg_sink = []

        packet = Packet(self.cnt, self.data[self.cnt], self)
        self.cnt += 1
        if rand_l():
            self.receiver.put(packet)
        self.sleep()

    def sleep(self):
        self.time += self.rand_t()

    def get_loss_msg(self, serial_num):
        self.msg_sink.append(serial_num)


class Receiver:
    def __init__(self, id, size, rand_t, delay=0):
        self.id = id
        self.size = size
        self.cnt = 0
        self.data_sink = {}
        self.data_ptr = {}
        self.data_cnt = {}
        self.address = {}
        self.output = [-1] * size
        self.rand_t = rand_t
        self.time = delay

    def register(self, sender):
        self.data_sink[sender.id] = [-1] * self.size
        self.data_ptr[sender.id] = 0
        self.data_cnt[sender.id] = 0
        self.address[sender.id] = sender

    def put(self, packet, resend=False):
        p_src = packet.src.id
        p_serial = packet.serial_num
        p_data = packet.data
        self.data_sink[p_src][p_serial] = p_data
        if resend == False:
            self.data_cnt[p_src] += 1

    def awake(self):
        self.check_loss()
        self.add_data()
        self.sleep()

    def check_loss(self):
        for sender in self.data_sink.keys():
            temp_data = self.data_sink[sender]
            temp_ptr = self.data_ptr[sender]
            temp_cnt = self.data_cnt[sender] + 1
            
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
            A.awake()
            print("A awake at : %.5f" %A.time)
            A_cnt += 1
        elif B.time <= A.time and B.time <= C.time:
            B.awake()
            print("B awake at : %.5f" %B.time)
            B_cnt += 1
        else:
            C.awake()
            print("C awake at : %.5f" %C.time)
            C_cnt += 1
        if A_cnt>=30 or B_cnt>=30 or C_cnt>=30:
            break
    print("The sum of the data received :", C.output)
    print("Sent Number for A :", C.data_sink['A'])
    print("Sent Number for B :", C.data_sink['B'])

if __name__ == '__main__':
	main()
