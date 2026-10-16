from __future__ import annotations
from typing import Callable
from unittest import TestCase


class _Channel:
	def __init__(self, name: str):
		"""
		:param name: the name of the channel
		"""
		self.name = name
		self.methods: dict[str, list[Callable]] = dict()

	def switch_methods(self, instance):
		for method_name, method in self.methods.items():
			setattr(instance, method_name, method.__get__(instance))


class _ChannelsEmbedding:
	"""
	This is what is/was supposed to be embedding in the test case classes.
	"""
	def __init__(self, class_name: str):
		self.class_name = class_name
		self.channels: dict[str, _Channel] = {}

	@property
	def channel_names(self) -> list[str]:
		return [name for name in self.channels.keys()]

	def activate_channel(self, channel_name: str, class_instance) -> None:
		channel_ = self.channels[channel_name]
		channel_.switch_methods(class_instance)

	def register_method_for_channel_name(self, method, channel_name: str):
		if self.channels.get(channel_name) is None:
			self.channels[channel_name] = _Channel(channel_name)
		channel = self.channels[channel_name]
		channel.methods[method.__name__] = method


_test_case_run_hijacked = False
_class_names_to_embeddings: dict["str", _ChannelsEmbedding]  = {}
_original_test_case_run = TestCase.run
def _replacement_testcase_run(self: TestCase, result):
	original_method = getattr(self, self._testMethodName)
	def _our_execution():
		embedding = _class_names_to_embeddings.get(type(self).__qualname__)
		if embedding is None:
			original_method()
		else:
			for channel_name in embedding.channels:
				embedding.activate_channel(channel_name, self)
				with self.subTest(channel_name):
					redone_test_case = type(self)(self._testMethodName)
					redone_test_case.run = _original_test_case_run
					redone_test_case.run(redone_test_case)
	try:
		setattr(self, self._testMethodName, _our_execution)
		return _original_test_case_run(self, result)
	finally:
		setattr(self, self._testMethodName, original_method)


# noinspection PyPep8Naming
class channel:
	channels: dict[str, "channel"] = {}

	@staticmethod
	def _read_class_name_from_method(method):
		return method.__qualname__.rsplit(".", 1)[0]

	@staticmethod
	def _acquire_or_make_embedding(class_name: str) -> _ChannelsEmbedding:
		embedding = _class_names_to_embeddings.get(class_name)
		if embedding is None:
			embedding = _ChannelsEmbedding(class_name)
		return embedding

	def __init__(self, name: str):
		self.name = name
		self.method = None

	def __call__(self, method):
		if not _test_case_run_hijacked:
			TestCase.run = _replacement_testcase_run
		class_name = self._read_class_name_from_method(method)
		embedding = self._acquire_or_make_embedding(class_name)
		embedding.register_method_for_channel_name(method, self.name)
		_class_names_to_embeddings[class_name] = embedding
		return method

