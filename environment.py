
from random import gauss
from random import random

def interval_rand():
    return 1 + gauss(0, 0.01)

def packet_loss_rand():
    return random() > 0.5

class Environment(object):

    def __init__(interval_rand, packet_loss_rand):
        self.interval_rand = interval_rand
        self.packet_loss_rand = packet_loss_rand
        self.timeline = []
        self.node = {}

    def run(self):

    def add(node):
