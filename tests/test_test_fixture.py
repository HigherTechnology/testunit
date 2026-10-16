from typing import Callable
from unittest import TestCase
from testunit import Fixture


class TestingFixture(Fixture):

	def __init__(self, on_setup: Callable[[], None], on_tear_down: Callable[[], None]):
		self._on_setup = on_setup
		self._on_tear_down = on_tear_down
		super().__init__()


	def setUp(self):
		self._on_setup()

	def tearDown(self):
		self._on_tear_down()


class TestTestFixture(TestCase):
	def setUp(self):
		self._setup_ran = False
		self._tear_down_ran = False
		def on_setup():
			self._setup_ran = True
		def on_tear_down():
			self._tear_down_ran = True
		self._fixture = TestingFixture(on_setup, on_tear_down)

	def test_should_run_setup_after_construction_as_expected(self):
		self.assertTrue(self._setup_ran)

	def test_should_run_tear_down_after_deleted_as_expected(self):
		del self._fixture
		self.assertTrue(self._tear_down_ran)

	def test_should_not_run_tear_down_before_deletion(self):
		self.assertFalse(self._tear_down_ran)

