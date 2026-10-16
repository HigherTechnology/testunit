import os
import tempfile
import unittest
from testunit import channel
from subprocess import check_call


# TODO test if this can fail as expected and decide behavior around that.
class TestMakingDirectories(unittest.TestCase):
	def setUp(self):
		self._temp_directory = tempfile.TemporaryDirectory()

	@channel("LinuxCommandLine")
	def _make_directory(self, path: str) -> None:
		check_call(["mkdir", path])

	@channel("OsModule")
	def _make_directory(self, path: str) -> None:
		os.mkdir(path)

	def test_should_create_something_at_path(self):
		path = os.path.join(self._temp_directory.name, "directory")
		self._make_directory(path)
		assert os.path.exists(path)

	def test_something_at_path_should_be_directory(self):
		path = os.path.join(self._temp_directory.name, "directory")
		self._make_directory(path)
		assert os.path.isdir(path)


class TestRunningTestsWithNoChannels(unittest.TestCase):

	def test_should_do_nothing_and_pass(self):
		pass
