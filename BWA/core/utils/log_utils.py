import inspect
import logging
import os

from django.conf import settings

from .user_utils import UserUtils

basedir = settings.BASE_DIR
logger = logging.getLogger('mgl')

'''
Classe générique de gestion des logs : permet d'harmoniser les logs de la manière suivante.
ex : $moduleName [$emailUser] $className.$methodName - $message
'''


class LogUtils:

    @staticmethod
    def __default():
        try:
            class_name = inspect.stack()[2][0].f_locals['self'].__class__.__name__
            class_object = inspect.stack()[2][0].f_locals['self'].__class__
            classpath = inspect.getfile(class_object)
        except:
            # Cas particulier des méthodes statiques.
            class_name = list(inspect.stack()[2][0].f_globals.keys())[-1]
            classpath = inspect.stack()[2][1]

        method_name = inspect.stack()[2][3]
        index_basedir = classpath.find(str(basedir))
        module_name = "NO_MODULE_FOUND" if index_basedir == -1 else classpath[len(str(basedir)) + 1:].split(os.path.sep)[0]
        user_email = UserUtils.get_current_authenticated_user_email()

        return f'{module_name} [{user_email}] {class_name}.{method_name}'

    @staticmethod
    def info(msg=None):
        logger.info(f'{LogUtils.__default()} - {msg}')

    @staticmethod
    def debug(msg=None):
        logger.debug(f'{LogUtils.__default()} - {msg}')

    @staticmethod
    def error(msg=None):
        logger.error(f'{LogUtils.__default()} - {msg}')
