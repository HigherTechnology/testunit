

class Fixture:
	def __init__(self):
		self.setUp()

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def __del__(self):
		self.tearDown()
