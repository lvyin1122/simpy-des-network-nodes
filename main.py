from Node import *

# 随机函数-时间间隔：根据题目设置为 1 + gauss(0, 0.01)
def rand_t():
    return 1 + gauss(0, 0.01)

# 随机函数-丢包概率：返回值为True时不发生丢包；此处设置为5%丢包率
def rand_l():
    return random() < 0.95

def main():
    # 初始化对象
    data = [i for i in range(1, 31)]
    C =Receiver('C', 30, rand_t)
    A = Sender('A', C, data, rand_t, rand_l)
    B = Sender('B', C, data, rand_t, rand_l)

    # 注册发送者
    C.register(A)
    C.register(B)

    # 模拟系统循环次数
    sim_time = 17
    A_cnt = 0
    B_cnt = 0
    C_cnt = 0
    print_time = sim_time - 2

    """
    模拟次数多余打印次数是因为：
    多余的模拟次数是为了修正前项的丢包，而最后一项若丢包则会无法修复。
    这属于系统误差，所以无需将这几项打印出来
    """

    # 打印输出显示时间间隔
    display_interval = 0

    # 模拟系统循环
    while True:
        if A.time <= B.time and A.time <= C.time:
            print('-%5.2fs- Sender awakes         | id:%3s' % (A.time, 'A'))
            A.awake()
            time.sleep(display_interval)
            A_cnt += 1
        elif B.time <= A.time and B.time <= C.time:
            print('-%5.2fs- Sender awakes         | id:%3s' % (B.time, 'B'))
            B.awake()
            time.sleep(display_interval)
            B_cnt += 1
        else:
            print('-%5.2fs- Receiver awakes       | id:%3s' % (C.time, 'C'))
            C.awake()
            time.sleep(display_interval)
            C_cnt += 1
        if A_cnt>=sim_time or B_cnt>=sim_time or C_cnt>=sim_time:
            break

    # 打印最终结果
    print("\nThe sum of the data received : ")
    for i in range(0,print_time):
	    print(C.output[i],end=", ")

    print("\n\nSent Number for A :")
    for i in range(0,print_time):
        print( C.data_sink['A'][i],end=", ")

    print("\n\nSent Number for B :")
    for i in range(0,print_time):
        print( C.data_sink['B'][i],end=", ")

if __name__ == '__main__':
	main()
