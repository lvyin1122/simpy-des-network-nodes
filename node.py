
class Packet(object):

    def __init__(self, src_id, serial_num, data):
        self.src_id = src_id
        self.serial_num = serial_num
        self.data = data

class Sender(object):

    def __init__(self, id, dataset):
        self.id = id
        self.dataset = dataset
        self.cnt = 0
        self.dst = None

    def send(self):
        data = dataset(cnt)
        packet = Packet(self.id, self.cnt, data)
        dst.put(packet)
        cnt += 1

    def resend(serial_num):
        data = dataset(cnt)
        packet = Packet(self.id, self.cnt, data)
        dst.put(packet)


class Receiver(object):

    def __init__(self, id):
        self.id = id
        self.sink = {} #字典类型，按id存储数组
        self.data = []
        self.

    def create_sink(self)     

    def connect(self)

    def put(packet):
