from django.conf import settings
from threading import local

COMMAND_ATTR_NAME = getattr(settings, 'LOCAL_COMMAND_NAME', '_current_command')

_thread_locals = local()


class CommandeUtils:

    @staticmethod
    def init(command_name):
        setattr(_thread_locals, COMMAND_ATTR_NAME, command_name)

    @staticmethod
    def is_command_running():
        return True if CommandeUtils.get_command_name() else False

    @staticmethod
    def get_command_name():
        return getattr(_thread_locals, COMMAND_ATTR_NAME, None)
