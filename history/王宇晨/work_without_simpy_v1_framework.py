#输出-接收模型的framework建立
"""
需要完善的内容：
1.Sender输出数据的产生方式（用什么方法产生1，2，3，4……）
2.这种数据产生方式是否方便进行修正以使得C接收的数据为（2，4，6，8……）

3，丢包后解决方法
"""


from random import gauss,random

class Sengding_number:
	def __init__(self,value,name):
		self.value = value
		self.name = name
		
class Sender:
	time = 0
	ser_num = 1
	def __init__(self,receiver,name):
		self.receiver = receiver
		self.name = name
		
	#def serial_num(self,src_id):
		
		
	def send(self):
		
		data = Sengding_number(self.ser_num,self.name)
		self.receiver.receive(data)
		self.sleep()

	def sleep(self):
		self.time += 1 + gauss(0,0.01)

class Receiver:
	time = 0
	latest_receive = {}
	add = []
	record = {}
	
	def __init__(self,name):
		self.name = name
		self.latest_receive['A'] = Sengding_number(0,'A')
		self.latest_receive['B'] = Sengding_number(0,'B')
		self.record['A'] = []
		self.record['B'] = []

	def receive(self,data):
		self.record[data.name].append(data.value)
		self.latest_receive[data.name] = data
	
	def add_data(self):
		self.add.append(self.latest_receive['A'].value + self.latest_receive['B'].value)
		self.sleep()

	def sleep(self):
		self.time += 1 + gauss(0,0.01)

def main():
	C =Receiver('C')
	A = Sender(C,'A')
	B = Sender(C,'B')
	A_cnt = 0
	B_cnt = 0
	C_cnt = 0
	while True:
		if A.time <= B.time and A.time <= C.time:
			A.send()
			print("A awake at : %.5f" %A.time)
			A_cnt += 1
		elif B.time <= A.time and B.time <= C.time:
			B.send()
			print("B awake at : %.5f" %B.time)
			B_cnt += 1
		else:
			C.add_data()
			print("C awake at : %.5f" %C.time)
			C_cnt += 1
		if A_cnt>30 or B_cnt>30 or C_cnt>30:
			break
	print("The sum of the data received :", C.add)
	print("Sent Number for A :", C.record['A'])
	print("Sent Number for B :", C.record['B'])

if __name__ == '__main__':
	main()
