name = "rss"
class Test(object):
	"""docstring for Test"""
	def __init__(self, user):
		super(Test, self).__init__()
		self.userName = user
	def printName(self):
		print self.userName
if __name__ == "__main__":
	 a = Test("ruansongsong")
	 a.printName()
		