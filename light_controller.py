from spidev import SpiDev
import time


class LightController(object):
	def __init__(self, bus = 0, device = 0, pins = 24):
		self.bus = bus
		self.device = device
		self.spi = SpiDev()
		self.spi.open(bus, device)

		self.MAX = 0xfff
		self.MIN = 0x000
		self.pins = pins
		self.light_values = [0 for _ in range(36)]
		self.send()
		self.scanning = 0
		self.map = {0:1, 1:2, 2:4, 3:5, 4:7, 5:8, 6:10, 7:11, 8:13, 9:14, 10:16, 11:17, 12:19, 13:20, 14:22, 15:23, 16:25, 17:26, 18:28, 19:29, 20:31, 21:32, 22:34, 23:35}
	
		self.clear()
			

	def set(self, pin, val):
		assert(pin < self.pins and pin >= 0)
		if (val >= self.MAX): val = self.MAX
		if (val < self.MIN): val = self.MIN	
		actual = self.map[pin]
		self.light_values[actual] = val
 
	def send(self):
		self.spi.xfer(self.light_values[::-1])

	def pic_countdown(self, init_delay = 1, delay = 1):
		time.sleep(init_delay)	
		for i in range(0, 4):
			self.set(i, self.MAX)
		self.send()
		time.sleep(delay)	
		for i in range(4, 8):
			self.set(i, self.MAX)
		self.send()
		time.sleep(delay)	
		for i in range(8, 12):
			self.set(i, self.MAX)
		self.send()
		time.sleep(delay)	
		for i in range(12, 16):
			self.set(i, self.MAX)
		self.send()
		time.sleep(3)
		self.clear()
	
	def scan(self):
		self.clear()
		for i in range(0, 10, 2):
			self.set(i, self.MAX)
			self.set(i + 1, self.MAX)
			self.send()
			time.sleep(0.2)
			self.clear()

		for i in range(11, -1, -2):
			self.set(i, self.MAX)
			self.set(i - 1, self.MAX)
			self.send()
			time.sleep(0.2)
			self.clear()

	def scan_success(self):
		self.clear()
		self.set(12, self.MAX)
		self.set(13, self.MAX)
		self.set(14, self.MAX)
		self.set(15, self.MAX)
		self.send()
		time.sleep(3)
		self.clear()
			
	def cycle(self):
		for i in range(len(self.light_values)):
			self.set(i, self.MAX)
			self.send()
			print('Light ' + str(i) + " is on")
			time.sleep(1)	
			self.set(i, self.MIN)
			self.send()
		
	def test(self):
		num = ""
		while num != "quit":
			num = int(input("which light to get lit? "))
			self.clear()
			self.set(num, self.MAX)
			self.send()


	def clear(self):
		for i in range(0, self.pins):
			self.set(i, self.MIN)
		self.send()

	def __del__(self):
		self.spi.close()

if __name__ == "__main__":
	lc = LightController(pins = 24)
	lc.test()
	#lc.pic_countdown(delay = 1)
	#lc.scan()
