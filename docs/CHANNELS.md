## What is a channel?

A channel is a channel to go through to get what you're testing. Simplest scenario for a channel: Change the channel and you change what you are testing. You could have a test for making directories and a method to make a directory, one channel would make the method for making a directory use os.mkdir, and another os.system.

## How do you use a channel?

You put the channel decorator on top of a method. The first time you use a channel on a method that channel is created and the method you put it on will be the method used for that name when running with that channel. Channels are named with strings and referenced later by strings. 

### Channels By Example -> Different Methods

```py
import os
import tempfile
import unittest
from testunit import channel
from subprocess import check_call


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

``